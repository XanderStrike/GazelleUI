import torrent as torrent

def job_list():
  return [
    {
      'id': 'torrents',
      'func': '__main__:jobs.download_torrents',
      'trigger': 'interval',
      'seconds': 10
    }
  ]

def download_torrents():
  torrent.download_all()
