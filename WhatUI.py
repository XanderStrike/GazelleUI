# WhatUI
#   https://github.com/XanderStrike/WhatUI

import os
import sys

# === Settings ===

# Access
#   Set BIND to localhost to hide from the big scary internet internet
PORT = 2020
BIND = '0.0.0.0'

# Where to save .torrent files
#   Must end in a slash
DOWNLOAD_PATH = 'torrents/'

# ================

from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, Response
import whatapi

from lib.auth import requires_auth
import lib.settings as settings

app = Flask(__name__)
app.config.update(DEBUG=True)

# Initialize Settings
settings.init_db()

# Try to login to whatcd
try:
  setting = settings.get('what_credentials')
  print setting
  apihandle = whatapi.WhatAPI(username=setting[1], password=setting[2])
except:
  print "What.cd username and password incorrect"
  print "Add them on the settings page then restart!"


# Methods
def get_artist_results(query):
  try:
    return apihandle.request('artist', artistname=query)['response']
  except whatapi.whatapi.RequestException:
    return "an error"


# Routes
@app.route("/")
@requires_auth
def index():
  return render_template('index.html')

@app.route("/search")
@requires_auth
def search():
  query = request.args['q']
  results = get_artist_results(query)
  return render_template('search.html', results=results)

@app.route("/want")
@requires_auth
def want():
  torrent_id = request.args['id']
  download_link = 'https://ssl.what.cd/torrents.php?action=download&id=' + torrent_id + '&authkey=' + apihandle.authkey + '&torrent_pass=' + apihandle.passkey
  os.system("wget -bq \"" + download_link + "\" -O " + DOWNLOAD_PATH + torrent_id + ".torrent")
  return "Fetched!"

@app.route("/group_info")
@requires_auth
def group_info():
  group_id = request.args['id']
  results = apihandle.request('torrentgroup', id=group_id)['response']['group']
  return render_template('group_info.html', group_info=results)

@app.route("/settings", methods=['GET', 'POST'])
@requires_auth
def settings_path():
  output = ''
  if request.method == 'POST':
    output = settings.update(request.form)
  return render_template('settings.html', settings=settings.get_all(), output=output)


# Serve Static Assets
@app.route('/assets/<path:filename>')
def send_assets(filename):
    return send_from_directory('assets', filename)


# It's Go Time
if __name__ == "__main__":
  app.run(host=BIND, port=PORT)
