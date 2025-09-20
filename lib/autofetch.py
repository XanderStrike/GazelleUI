from . import database
from . import torrent
from . import wat
from enum import Enum

# https://www.notinventedhere.org/articles/python/how-to-use-strings-as-name-aliases-in-python-enums.html
mappings = Enum(
    value='mappings',
    names=[
        ('Album', 1),
        ('Soundtrack', 3),
        ('EP', 5),
        ('Anthology', 6),
        ('Compilation', 7),
        ('Single', 9),
        ('Live album', 11),
        ('Remix', 13),
        ('Bootleg', 14),
        ('Interview', 15),
        ('Mixtape', 16),
        ('Demo', 17),
        ('Concert Recording', 18),
        ('DJ Mix', 19),
        ('Unknown', 21)
    ]
)

def create_subscription(data):
  query = 'insert into subscriptions(search_type, term, quality, release_type) values (' + \
          '"' + data['search_type'] + '", ' + \
          '"' + data['term'] + '", ' + \
          '"' + data['quality'] + '", ' + \
          '"' + data['release_type'] + '")'

  database.update(query)

def enqueue(data):
  if not torrent.exists(data['id'], data['artist'], data['album']):
    print("Downloading")
    torrent.queue(data)
  else:
    print("Skipping, already downloaded")

def fetch_new_torrents(sub):
  print(sub['search_type'] + ' search for "' + sub['term'] + \
    '" with quality ' + sub['quality'] + ' and release type ' + str(sub['release_type']))

  if sub['search_type'] == 'artist':
    data = wat.get_artist(sub['term'])

    if data == 'no data':
      print('Nothing found')
      return

    for group in data['torrentgroup']:
      if int(group['releaseType']) == int(sub['release_type']):
        for t in group['torrent']:
          if t['encoding'] == sub['quality']:
            print("Found " + group['groupName'] + ' (' + str(t['id']) + ')')
            t.update({
              'artist': data['name'],
              'album': group['groupName']
            })
            enqueue(t)
            break
  
def run():
  for sub in database.subscriptions():
    fetch_new_torrents(sub)
