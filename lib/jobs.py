import torrent as torrent
import wat as wat
import autofetch as af

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
    },
    {
      'id': 'autofetch',
      'func': '__main__:jobs.autofetch',
      'trigger': 'interval',
      'seconds': 11520
    }
  ]

def download_torrents():
  torrent.download_all()

def update_user():
  print 'Updating user info'
  wat.refresh_user_info()

def autofetch():
  af.run()
