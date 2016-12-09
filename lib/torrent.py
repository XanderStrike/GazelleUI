import database as database
import wat as wat
import settings as settings
import json

import urllib2

def queue(data):
  data = json.loads(data)
  query = 'insert into torrents(id, artist, album, release, quality, added, downloaded) values ("' + \
    str(data['id']) + '", "' + \
    data['artist'] + '", "' + \
    data['album'] + '", "' + \
    data['displayTitle'] + '", "' + \
    data['media'] + " / " + data['format'] + " " + \
    data['encoding'] + '", ' + \
    'datetime("now"), 0)'

  database.update(query)

def download_all():
  torrents = database.row_fetch('select * from torrents where downloaded = 0')
  for t in torrents:
    download_torrent(t[0])

def download_torrent(torrent_id):
  download_link = wat.download_link(torrent_id)
  download_path = settings.get('torrent')[1]
  save_to = download_path + torrent_id + ".torrent"

  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  torrent = opener.open(download_link).read()

  output = open(save_to,'wb')
  output.write(torrent)
  output.close()

  print "Downloaded " + torrent_id + ".torrent"
  database.update('update torrents set downloaded = 1 where id = "' + torrent_id + '"')

def get_recent():
  return database.row_fetch('select * from torrents order by added desc limit 20')

def get_all():
  return database.row_fetch('select * from torrents order by added desc')

def get_ids_for_artist(artist):
  return database.fetch('select id from torrents where artist = "' + artist + '"')

def get_all_ids():
  return database.fetch('select id from torrents')
