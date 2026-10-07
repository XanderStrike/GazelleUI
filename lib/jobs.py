from . import torrent as torrent
from . import wat as wat
from . import autofetch as af

def job_list():
  return [
    {
      'id': 'torrents',
      'func': 'lib.jobs:download_torrents',
      'trigger': 'interval',
      'seconds': 10
    },
    {
      'id': 'update_user_info',
      'func': 'lib.jobs:update_user',
      'trigger': 'interval',
      'seconds': 900
    },
    {
      'id': 'autofetch',
      'func': 'lib.jobs:autofetch',
      'trigger': 'interval',
      'seconds': 11520
    }
  ]

def download_torrents():
  torrent.download_all()

def update_user():
  print('Updating user info')
  try:
    wat.refresh_user_info()
  except wat.UpstreamError as e:
    print('Skipping user info update: ' + e.message)

def autofetch():
  try:
    af.run()
  except wat.UpstreamError as e:
    print('Skipping autofetch: ' + e.message)
