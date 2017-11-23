import database
import torrent
import wat

def word_to_type(release_type):
  mapping = {
    'Album': 1,
    'Soundtrack': 3,
    'EP': 5,
    'Anthology': 6,
    'Compilation': 7,
    'Single': 9,
    'Live album': 11,
    'Remix': 13,
    'Bootleg': 14,
    'Interview': 15,
    'Mixtape': 16,
    'Unknown': 21,
    'Demo': 23
  }

  return mapping[release_type]

def enqueue(data):
  if not torrent.exists(data['id'], data['artist'], data['album']):
    print "Downloading"
    torrent.queue(data)
  else:
    print "Skipping, already downloaded"

def run():
  for sub in database.subscriptions():
    print sub['search_type'] + ' search for "' + sub['term'] + \
      '" with quality ' + sub['quality'] + ' and release type ' + str(sub['release_type'])

    if sub['search_type'] == 'artist':
      data = wat.get_artist(sub['term'])

      for group in data['torrentgroup']:
        if group['releaseType'] == sub['release_type']:
          for t in group['torrent']:
            if t['encoding'] == sub['quality']:
              print "Found " + group['groupName'] + ' (' + str(t['id']) + ')'
              t.update({
                'artist': data['name'],
                'album': group['groupName']
              })
              enqueue(t)
              break
    elif sub['search_type'] == 'label':
      data = wat.label(sub['term'])

      for res in data['results']:
        if word_to_type(res['releaseType']) == sub['release_type']:
          for t in res['torrents']:
            if t['encoding'] == sub['quality']:
              print 'Found ' + res['groupName']
              t.update({
                'artist': res['artist'],
                'album': res['groupName']
                })
              enqueue(t)
              break





