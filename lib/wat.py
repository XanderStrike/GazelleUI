import whatapi
import settings as settings
import torrent as torrents

import json

apihandle = None


# Login stuff
def handle():
  global apihandle
  try:
    setting = settings.get('what_credentials')
    domain = settings.get('domain')[1]
    if apihandle != None:
      return apihandle
    apihandle = whatapi.WhatAPI(username=setting[1], password=setting[2], domain=domain)
    return apihandle
  except:
    raise Exception('Something went wrong connecting to WhatCD. Ensure that it is up and running, and that your credentials are correct.')

def bust_handle_cache():
  global apihandle
  apihandle = None


# Fetching
def get_artist(query):
  try:
    info = handle().request('artist', artistname=query)['response']
    return handle_artist_results(info)
  except whatapi.whatapi.RequestException:
    return "I should really do something here"

def get_group(group_id):
  try:
    return handle().request('torrentgroup', id=group_id)['response']['group']
  except:
    return "I should really do something here"

def browse(searchstr):
  try:
    info = handle().request('browse', searchstr=searchstr)['response']
    return handle_browse_results(info)
  except:
    return "I should really do something here"

def label(searchstr):
  try:
    info = handle().request('browse', recordlabel=searchstr)['response']
    return handle_browse_results(info)
  except:
    return "I should really do something here"

def download_link(torrent_id):
  domain = settings.get('domain')[1]
  return domain + '/torrents.php?action=download&id=' + torrent_id + '&authkey=' + handle().authkey + '&torrent_pass=' + handle().passkey

# Massaging
def handle_browse_results(info):
  try:
    snatched_torrents = list(zip(*torrents.get_all_ids())[0])
  except IndexError:
    snatched_torrents = []


  for res in info.get('results'):
    for torrent in res.get('torrents'):

      if str(torrent.get('torrentId')) in snatched_torrents:
        torrent['alreadySnatched'] = 1
      else:
        torrent['alreadySnatched'] = 0

      make_browse_title(torrent)

      torrent['id'] = torrent['torrentId']
      torrent['size'] = human_readable(torrent['size'])
      torrent['artist'] = res['artist']
      torrent['album'] = res['groupName']

      torrent['json'] = json.dumps(torrent)

  return info


def handle_artist_results(info):
  try:
    snatched_torrents = list(zip(*torrents.get_ids_for_artist(info['name']))[0])
  except IndexError:
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
    torrent['displayTitle'] = torrent.get('remasterTitle') + " / "
    torrent['displayTitle'] += torrent.get('remasterRecordLabel')

def make_browse_title(torrent):
  if torrent.get('remasterYear', 0) == 0:
    torrent['displayTitle'] = "Original Release"
  else:
    torrent['displayTitle'] = torrent.get('remasterTitle')

# http://stackoverflow.com/a/1094933/1855253
def human_readable(size):
  for unit in ['','K','M','G','T','P','E','Z']:
    if abs(size) < 1024.0:
        return "%3.1f%s%s" % (size, unit, 'B')
    size /= 1024.0
  return "%.1f%s%s" % (size, 'Y', 'B')
