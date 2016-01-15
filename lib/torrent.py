import database as database
import wat as wat
import settings as settings

import os

def queue(id):
  database.update('insert into torrents(id, added, downloaded) values ("' + id + '", datetime("now"), 0)')

def download_all():
  torrents = database.row_fetch('select * from torrents where downloaded = 0')
  for t in torrents:
    download_link = wat.download_link(t[0])
    download_path = settings.get('torrent')[1]
    os.system("wget -bq \"" + download_link + "\" -O " + download_path + t[0] + ".torrent")
    print "Downloaded " + t[0] + ".torrent"
    database.update('update torrents set downloaded = 1 where id = "' + t[0] + '"')
