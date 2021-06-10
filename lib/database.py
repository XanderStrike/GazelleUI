import sqlite3 as lite

SCHEMA = {
  'settings':
    [
      "key PRIMARY KEY",
      "value_1",
      "value_2"
    ],
  'torrents':
    [
      'id PRIMARY KEY',
      'artist',
      'album',
      'release',
      'quality',
      'added DATETIME',
      'downloaded BOOLEAN'
    ],
  'user':
    [
      'username PRIMARY KEY',
      'upload',
      'download',
      'ratio',
      'requiredratio',
      'class',
      'notifications',
      'newSubscriptions',
      'messages',
      'newBlog'
    ],
  'subscriptions':
    [
      'id INTEGER PRIMARY KEY AUTOINCREMENT',
      'search_type',
      'term',
      'quality',
      'release_type'
    ]
}

DEFAULT_SETTINGS = [
  ['what_credentials', '', ''],
  ['webui_credentials', '', ''],
  ['network', '0.0.0.0', '2020'],
  ['torrent', '/torrents/', ''],
  ['domain', 'https://apollo.rip', ''],
  ['discord', '', '']
]

DB = 'config/data.sqlite3'

def init():
  con = lite.connect(DB)

  for k in list(SCHEMA.keys()):
    con.cursor().execute("create table if not exists " + k + "(" + ", ".join(SCHEMA[k]) + ");")

  for setting in DEFAULT_SETTINGS:
    con.cursor().execute("insert into settings(key, value_1, value_2) select '" + "', '".join(setting) + "' where not exists(select 1 from settings where key = '" + setting[0] + "')")

  con.commit()

  if (con.cursor().execute("select count(1) from user").fetchall() == [(0,)]):
    con.cursor().execute("insert into user(username) select ''")

  con.commit()

def update(query):
  con = lite.connect(DB)
  con.cursor().execute(query)
  con.commit()
  return True

def fetch(query):
  cur = lite.connect(DB).cursor()
  return cur.execute(query).fetchall()

def row_fetch(query):
  con = lite.connect(DB)
  con.row_factory = lite.Row
  return con.cursor().execute(query).fetchall()

def userinfo():
  return fetch('select * from user')[0]

def subscriptions():
  res = fetch('select search_type, term, quality, release_type, id from subscriptions')
  h = []
  for r in res:
    h.append({
      'search_type': r[0],
      'term': r[1],
      'quality': r[2],
      'release_type': r[3],
      'id': r[4]
      })

  return h

def delete_sub(id):
  update("delete from subscriptions where id = " + str(id))
