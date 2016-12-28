import torrent as torrent
import wat as wat

def job_list():
  return [
    {
      'id': 'torrents',
      'func': '__main__:jobs.download_torrents',
      'trigger': 'interval',
      'seconds': 10
    },
    {
      'id': 'update_user_info',
      'func': '__main__:jobs.update_user',
      'trigger': 'interval',
      'seconds': 900
    }
  ]

def download_torrents():
  torrent.download_all()

def update_user():
  print 'Updating user info'
  wat.refresh_user_info()
