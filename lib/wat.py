from . import whatapi
from . import settings as settings
from . import torrent as torrents
from . import database as database
from .whatapi.whatapi import RequestException, LoginException, ConnectionException
from requests.utils import cookiejar_from_dict

import time

apihandle = None
cache = {}
torrent_index = {}  # torrent_id -> enriched torrent dict
CACHE_DURATION = 24 * 60 * 60  # 24 hours in seconds


def display_domain():
  """The tracker hostname, for use in user-facing messages."""
  try:
    return settings.get('domain')[1].replace('https://', '').replace('http://', '').strip('/')
  except Exception:
    return 'the tracker'


def connection_reason(e):
  """Turn a requests connection error into a short, user-friendly reason."""
  text = str(e)
  if 'No route to host' in text:
    return 'no route to host — the tracker looks down or is blocked from this server'
  if 'Name or service not known' in text or 'nodename nor servname' in text or 'Name resolution' in text or 'Temporary failure in name resolution' in text:
    return 'could not resolve the domain'
  if 'Connection refused' in text:
    return 'connection refused'
  if 'timed out' in text or 'timeout' in text.lower():
    return 'connection timed out'
  if 'certificate' in text.lower() or 'SSL' in text:
    return 'TLS/SSL error'
  return 'connection failed'


class UpstreamError(Exception):
  """The tracker could not be reached or answered with an error.

  Carries a `title` and `message` suitable for showing in the web UI or API.
  """
  def __init__(self, message, title='Tracker unavailable'):
    super().__init__(message)
    self.message = message
    self.title = title


# Login stuff
def handle():
  global apihandle
  if apihandle != None:
    return apihandle
  try:
    setting = settings.get('what_credentials')
    cookie = None
    if settings.get('what_auth')[1]:
        cookie = cookiejar_from_dict({"session":settings.get('what_auth')[1]})

    domain = settings.get('domain')[1]
    apihandle = whatapi.WhatAPI(username=setting[1], password=setting[2], cookies=cookie, domain=domain)
    return apihandle
  except ConnectionException as e:
    print(f'Tracker connection error: {e}')
    raise UpstreamError(
      f"Could not connect to {display_domain()} ({connection_reason(e)}). "
      "The tracker may be down or unreachable from this server — check the domain in Settings and try again later.")
  except RequestException as e:
    if hasattr(e, 'response') and e.response is not None:
        status_code = e.response.status_code
        body = e.response.text
        raise UpstreamError(f'Request to the tracker failed with status code {status_code}. Response: {body}')
    else:
        raise UpstreamError(f'Request to the tracker failed: {str(e)}')
  except LoginException as e:
    raise UpstreamError(
      f'Login to {display_domain()} failed. Check your tracker credentials or session cookie in Settings.',
      title='Tracker login failed')
  except UpstreamError:
    raise
  except Exception as e:
    raise UpstreamError(f'Something went wrong connecting to the tracker: {str(e)}')

def bust_handle_cache():
  global apihandle
  apihandle = None

def bust_response_cache():
  global cache, torrent_index
  cache = {}
  torrent_index = {}

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
  except ConnectionException as e:
    print(f'Tracker connection error: {e}')
    raise UpstreamError(f"Could not connect to {display_domain()} ({connection_reason(e)})")
  except RequestException:
    return "no data"

def get_group(group_id):
  cache_key = f"group_{group_id}"
  if is_cache_valid(cache_key):
    return cache[cache_key]['data']

  try:
    result = handle().request('torrentgroup', id=group_id)['response']['group']
    cache[cache_key] = {'data': result, 'timestamp': time.time()}
    return result
  except ConnectionException as e:
    print(f'Tracker connection error: {e}')
    raise UpstreamError(f"Could not connect to {display_domain()} ({connection_reason(e)})")
  except RequestException:
    return "no data"

def download_link(torrent_id, use_token=None):
  domain = settings.get('domain')[1]

  # If use_token is explicitly specified, use that; otherwise check settings
  if use_token is None:
    use_tokens_setting = settings.get('use_tokens')
    token_count = use_tokens_setting[2] if use_tokens_setting[2] else '0'
    use_token = use_tokens_setting[1] == 'true' and int(token_count) > 0

  url = domain + '/torrents.php?action=download&id=' + torrent_id + '&authkey=' + handle().authkey + '&torrent_pass=' + handle().passkey
  if use_token:
    url += '&usetoken=1'

  print(url)

  return url

def refresh_user_info():
  info = handle().request('index')['response']

  # Update main user info
  database.update("update user set username = ?, "
                  "upload = ?, "
                  "download = ?, "
                  "ratio = ?, "
                  "requiredratio = ?, "
                  "class = ?, "
                  "notifications = ?, "
                  "newSubscriptions = ?, "
                  "messages = ?, "
                  "newBlog = ?",
                  (
                    info['username'],
                    human_readable(info['userstats']['uploaded']),
                    human_readable(info['userstats']['downloaded']),
                    str(info['userstats']['ratio']),
                    str(info['userstats']['requiredratio']),
                    str(info['userstats']['class']),
                    str(info['notifications']['notifications']),
                    str(info['notifications']['newSubscriptions']),
                    str(info['notifications']['messages']),
                    str(info['notifications']['newBlog']),
                  )
    )

  # Update token count
  gift_tokens = info.get('giftTokens', 0)
  merit_tokens = info.get('meritTokens', 0)
  total_tokens = gift_tokens + merit_tokens
  database.update("update settings set value_2 = ? where key = 'use_tokens'", (str(total_tokens),))

# Lookup
def get_torrent_info(torrent_id):
  """Look up enriched torrent data by ID from cache, or fetch from tracker."""
  tid = str(torrent_id)
  if tid in torrent_index:
    return torrent_index[tid]

  # Fall back to tracker API
  try:
    result = handle().request('torrent', id=tid)['response']['torrent']
    group = handle().request('torrentgroup', id=result.get('group', {}).get('id'))['response']['group']
    # Enrich to match handle_artist_results format
    result['artist'] = group.get('artist', '')
    result['album'] = group.get('name', '')
    make_artist_title(group, result)
    result['size'] = human_readable(result.get('size', 0))
    result['alreadySnatched'] = result.get('alreadySnatched', 0)
    torrent_index[tid] = result
    return result
  except UpstreamError:
    raise
  except Exception:
    return None

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

      # Index by torrent_id for lookup
      torrent_index[str(torrent.get('id'))] = torrent

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
