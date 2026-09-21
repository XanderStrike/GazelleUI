from . import database as database
from . import wat as wat
from . import settings as settings
from . import discord as discord
import json

import urllib.request, urllib.error, urllib.parse

class DuplicateError(Exception):
    pass

def queue(data):
  torrent_id = str(data['id'])
  artist = data['artist']
  album = data['album']

  if exists(torrent_id, artist, album):
    raise DuplicateError(f'torrent {torrent_id} already queued')

  query = 'insert into torrents(id, artist, album, release, quality, added, downloaded) values (?, ?, ?, ?, ?, datetime("now"), 0)'

  database.update(query, (
    torrent_id,
    artist,
    album,
    data['displayTitle'],
    data['media'] + " / " + data['format'] + " " + data['encoding'],
  ))

def exists(id, artist, album):
  query = 'select id from torrents where id = ? or (artist = ? and album = ?)'
  return database.fetch(query, (str(id), artist, album)) != []

def download_all():
  torrents = database.row_fetch('select * from torrents where downloaded = 0')
  for t in torrents:
    download_torrent(t[0])
    print('Downloaded ' + t[0] + '.torrent -- ' + t[1] + ' - ' + t[2] + ' / ' + t[3] + ' / ' + t[4])
    discord.send('Downloaded ' + t[1] + ' - ' + t[2] + ' / ' + t[3] + ' / ' + t[4])

def download_torrent(torrent_id):
  download_path = settings.get('torrent')[1]
  save_to = download_path + torrent_id + ".torrent"

  opener = urllib.request.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]

  # First attempt with token (if enabled in settings)
  download_url = wat.download_link(torrent_id)
  torrent = opener.open(download_url).read()

  # Check if we ran out of tokens, retry without token
  if b'You do not have any freeleech tokens left' in torrent:
    print("No freeleech tokens left, retrying without token")
    download_url = wat.download_link(torrent_id, use_token=False)
    torrent = opener.open(download_url).read()

  output = open(save_to,'wb')
  output.write(torrent)
  output.close()

  print("Downloaded " + torrent_id + ".torrent")
  database.update('update torrents set downloaded = 1 where id = ?', (torrent_id,))

def get_recent():
  return database.row_fetch('select * from torrents order by added desc limit 10')

def get_all(status=None, limit=None):
  query = 'select * from torrents'
  if status == 'queued':
    query += ' where downloaded = 0'
  elif status == 'downloaded':
    query += ' where downloaded = 1'
  query += ' order by added desc'
  if limit:
    query += f' limit {int(limit)}'
  return database.row_fetch(query)

def get_ids_for_artist(artist):
  return database.fetch('select id from torrents where artist = ?', (artist,))

def get_all_ids():
  return database.fetch('select id from torrents')
