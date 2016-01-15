import sqlite3 as lite

SCHEMA = {
  'settings':
    [
      "key PRIMARY KEY",
      "value_1",
      "value_2"
    ]
}

DEFAULT_SETTINGS = [
  ['what_credentials', '', ''],
  ['webui_credentials', '', ''],
  ['network', '0.0.0.0', '2020'],
  ['torrent', 'torrents/', '']
]

DB = 'data.sqlite3'

def init():
  con = lite.connect(DB)
  try:
    con.cursor().execute("select * from " + SCHEMA.keys()[0])
  except lite.OperationalError:
    print "No DB found, creating..."
    for k in SCHEMA.keys():
      con.cursor().execute("create table " + k + "(" + ", ".join(SCHEMA[k]) + ");")
    for setting in DEFAULT_SETTINGS:
      con.cursor().execute("insert into settings values ('" + "', '".join(setting) + "')");
      con.commit()

def update(query):
  conn = lite.connect(DB)
  conn.cursor().execute(query)
  conn.commit()
  return True

def fetch(query):
  cur = lite.connect(DB).cursor()
  return cur.execute(query).fetchall()

def row_fetch(query):
  con = lite.connect(DB)
  con.row_factory = lite.Row
  return con.cursor().execute(query).fetchall()
