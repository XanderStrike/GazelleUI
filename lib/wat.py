from . import whatapi
from . import settings as settings
from . import torrent as torrents
from . import database as database
from .whatapi.whatapi import RequestException, LoginException
from requests.utils import cookiejar_from_dict

import json
import time

apihandle = None
cache = {}
CACHE_DURATION = 24 * 60 * 60  # 24 hours in seconds


# Login stuff
def handle():
  global apihandle
  try:
    setting = settings.get('what_credentials')
    cookie = None
    if settings.get('what_auth')[1]:
        cookie = cookiejar_from_dict({"session":settings.get('what_auth')[1]})

    domain = settings.get('domain')[1]
    if apihandle != None:
      return apihandle
    apihandle = whatapi.WhatAPI(username=setting[1], password=setting[2], cookies=cookie, domain=domain)
    return apihandle
  except RequestException as e:
    if hasattr(e, 'response') and e.response is not None:
        status_code = e.response.status_code
        body = e.response.text
        raise Exception(f'Request to WhatCD failed with status code {status_code}. Response: {body}')
    else:
        raise Exception(f'Request to WhatCD failed: {str(e)}')
  except LoginException as e:
    raise Exception(f'Login to WhatCD failed: {str(e)}')
  except Exception as e:
    raise Exception(f'Something went wrong connecting to WhatCD: {str(e)}')

def bust_handle_cache():
  global apihandle
  apihandle = None

def bust_response_cache():
  global cache
  cache = {}

def is_cache_valid(cache_key):
  if cache_key not in cache:
    return False
  return time.time() - cache[cache_key]['timestamp'] < CACHE_DURATION


# Fetching
def get_artist(query):
  cache_key = f"artist_{query}"
  if is_cache_valid(cache_key):
    return cache[cache_key]['data']

  try:
    info = handle().request('artist', artistname=query)['response']
    result = handle_artist_results(info)
    cache[cache_key] = {'data': result, 'timestamp': time.time()}
    return result
  except whatapi.whatapi.RequestException:
    return "no data"

def get_group(group_id):
  cache_key = f"group_{group_id}"
  if is_cache_valid(cache_key):
    return cache[cache_key]['data']

  try:
    result = handle().request('torrentgroup', id=group_id)['response']['group']
    cache[cache_key] = {'data': result, 'timestamp': time.time()}
    return result
  except:
    return "no data"

def download_link(torrent_id):
  domain = settings.get('domain')[1]
  use_tokens_setting = settings.get('use_tokens')
  token_count = use_tokens_setting[2] if use_tokens_setting[2] else '0'
  use_tokens = use_tokens_setting[1] == 'true' and int(token_count) > 0

  url = domain + '/torrents.php?action=download&id=' + torrent_id + '&authkey=' + handle().authkey + '&torrent_pass=' + handle().passkey
  if use_tokens:
    url += '&usetoken=1'

  print(url)

  return url

def refresh_user_info():
  info = handle().request('index')['response']

  # Update main user info
  database.update("update user set username = '" + info['username'] + "', "
                  "upload = '" + human_readable(info['userstats']['uploaded']) + "', "
                  "download = '" + human_readable(info['userstats']['downloaded']) + "', "
                  "ratio = '" + str(info['userstats']['ratio'] )+ "', "
                  "requiredratio = '" + str(info['userstats']['requiredratio']) + "', "
                  "class = '" + str(info['userstats']['class']) + "', "
                  "notifications = '" + str(info['notifications']['notifications']) + "', "
                  "newSubscriptions = '" + str(info['notifications']['newSubscriptions']) + "', "
                  "messages = '" + str(info['notifications']['messages']) + "', "
                  "newBlog = '" + str(info['notifications']['newBlog']) + "'"
    )

  # Update token count
  gift_tokens = info.get('giftTokens', 0)
  merit_tokens = info.get('meritTokens', 0)
  total_tokens = gift_tokens + merit_tokens
  database.update("update settings set value_2 = '" + str(total_tokens) + "' where key = 'use_tokens'")

# Massaging
def handle_artist_results(info):
  snatched_torrents = []

  for group in info.get("torrentgroup", []):
    for torrent in group.get("torrent", []):
      make_artist_title(group, torrent)

      if str(torrent.get('id')) in snatched_torrents:
        torrent['alreadySnatched'] = 1
      else:
        torrent['alreadySnatched'] = 0

      torrent['size'] = human_readable(torrent['size'])

      torrent['artist'] = info['name']
      torrent['album'] = group['groupName']
      torrent['json'] = json.dumps(torrent)

  return info

def make_artist_title(group, torrent):
  if torrent.get('remasterYear', 0) == 0:
    torrent['displayTitle'] = "Original Release"
    if group.get("groupRecordLabel") != '':
      torrent['displayTitle'] += " / " + group.get("groupRecordLabel")
  else:
    torrent['displayTitle'] = str(torrent.get('remasterYear')) + " / "
    torrent['displayTitle'] += torrent.get('remasterRecordLabel')


# http://stackoverflow.com/a/1094933/1855253
def human_readable(size):
  for unit in ['','K','M','G','T','P','E','Z']:
    if abs(size) < 1024.0:
        return "%3.1f%s%s" % (size, unit, 'B')
    size /= 1024.0
  return "%.1f%s%s" % (size, 'Y', 'B')
