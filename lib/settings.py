import os
import secrets
from . import database as database

def get_or_create(key, generator_fn):
    try:
        current = get(key)
        if current and current[1]:
            return current[1]
    except (IndexError, KeyError):
        pass
    value = generator_fn()
    update({'setting': key, 'value_1': value, 'value_2': ''})
    return value

def update(params):
  try:
    database.update('insert or replace into settings(key, value_1, value_2) values (?, ?, ?)',
                    (params['setting'], params['value_1'], params['value_2']))
    return {'class': 'alert-success', 'message': 'Settings updated successfully.'}
  except:
    print("Error updating settings")
    return {'class': 'alert-error', 'message': 'Sorry but something went wrong! Check the log for details.'}

def get_all():
  s_list = database.row_fetch('select * from settings')
  s_dict = {}
  for setting in s_list:
    s_dict[setting['key']] = setting
  return s_dict

def get(key):
  return database.fetch('select * from settings where key = ?', (key,))[0]
