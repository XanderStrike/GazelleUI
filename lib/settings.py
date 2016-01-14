# todo: refactor sqlite3 shit into a service
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

def init_db():
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

def update(params):
  try:
    conn = lite.connect(DB)
    conn.cursor().execute('insert or replace into settings(key, value_1, value_2) values ("' + params['setting'] + '", "' + params['value_1'] + '", "' + params['value_2'] + '")')
    conn.commit()
    return {'class': 'alert-success', 'message': 'Settings updated successfully.'}
  except:
    print "Error updating settings: " + sys.exc_info()[0]
    return {'class': 'alert-error', 'message': 'Sorry but something went wrong! Check the log for details.'}

def get_all():
  con = lite.connect(DB)
  con.row_factory = lite.Row
  s_list = con.cursor().execute('select * from settings').fetchall()
  s_dict = {}
  for setting in s_list:
    s_dict[setting['key']] = setting
  return s_dict

def get(key):
  cur = lite.connect(DB).cursor()
  return cur.execute('select * from settings where key = "' + key + '"').fetchall()[0]
