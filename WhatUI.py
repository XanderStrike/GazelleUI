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

# WhatCD credentials
#   Run with WHAT_USERNAME=name WHAT_PASSWORD=pass python server.py
#   Or change these values
try:
  USERNAME = os.environ['WHAT_USERNAME']
  PASSWORD = os.environ['WHAT_PASSWORD']
except:
  print "Set the WHAT_USERNAME and WHAT_PASSWORD environment variables."
  sys.exit()

# ================

from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, Response
import whatapi

from lib.auth import requires_auth

app = Flask(__name__)
app.config.update(DEBUG=True)


# Try to login to whatcd
try:
  apihandle = whatapi.WhatAPI(username=USERNAME, password=PASSWORD)
except whatapi.whatapi.LoginException:
  print "Username and password incorrect"
  sys.exit()


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
  return "ok"


# Serve Static Assets
@app.route('/assets/<path:filename>')
def send_assets(filename):
    return send_from_directory('assets', filename)


# It's Go Time
if __name__ == "__main__":
  app.run(host=BIND, port=PORT)
