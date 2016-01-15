def job_list():
  return [
    {
      'id': 'torrents',
      'func': '__main__:jobs.download_torrents',
      'args': (),
      'trigger': 'interval',
      'seconds': 2
    }
  ]

def download_torrents():
  print 'download_torrents job running...'

  print 'download_torrents job finised'
