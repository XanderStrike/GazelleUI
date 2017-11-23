import database
import torrent
import wat

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
              if not torrent.exists(t['id']):
                print "Downloading"
                t.update({
                    'artist': data['name'],
                    'album': group['groupName']
                })
                torrent.queue(t)
              else:
                print "Skipping, already downloaded"

              break
    elif sub['search_type'] == 'label':
      print 'fuck'





