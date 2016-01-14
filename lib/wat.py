import whatapi
import lib.settings as settings

apihandle = None

# Login stuff
def handle():
  global apihandle
  try:
    setting = settings.get('what_credentials')
    if apihandle != None:
      return apihandle
    apihandle = whatapi.WhatAPI(username=setting[1], password=setting[2])
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

def download_link(torrent_id):
  return 'https://ssl.what.cd/torrents.php?action=download&id=' + torrent_id + '&authkey=' + handle().authkey + '&torrent_pass=' + handle().passkey

# Massaging
def handle_artist_results(info):
  for group in info.get("torrentgroup", []):
    for torrent in group.get("torrent", []):
      if torrent.get('remasterYear', 0) == 0:
        torrent['displayTitle'] = "Original Release"
        if group.get("groupRecordLabel") != '':
          torrent['displayTitle'] += " / " + group.get("groupRecordLabel")
      else:
        torrent['displayTitle'] = torrent.get('remasterTitle') + " / "
        torrent['displayTitle'] += torrent.get('remasterRecordLabel')

  return info
