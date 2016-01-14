# WhatUI
#   https://github.com/XanderStrike/WhatUI

import os
import sys

from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, Response

from lib.auth import requires_auth
import lib.settings as settings
import lib.wat as wat

app = Flask(__name__)
app.config.update(DEBUG=True)

# Initialize Settings
settings.init_db()


# Routes
@app.route("/")
@requires_auth
def index():
  setting = settings.get('what_credentials')
  if setting[1] == None or setting[1] == '':
    return render_template('settings.html', settings=settings.get_all(), message="Please set your whatcd username and password.", message_class="alert-error")
  return render_template('index.html')

@app.route("/search")
@requires_auth
def search():
  query = request.args['q']
  results = wat.get_artist(query)
  return render_template('search.html', results=results)

@app.route("/want")
@requires_auth
def want():
  torrent_id = request.args['id']
  download_link = wat.download_link(torrent_id)
  download_path = settings.get('torrent')[1]
  os.system("wget -bq \"" + download_link + "\" -O " + download_path + torrent_id + ".torrent")
  return "Fetched!"

@app.route("/group_info")
@requires_auth
def group_info():
  group_id = request.args['id']
  results = wat.get_group(group_id)
  return render_template('group_info.html', group_info=results)

@app.route("/settings", methods=['GET', 'POST'])
@requires_auth
def settings_path():
  output = {'message':None,'class':None}
  if request.method == 'POST':
    output = settings.update(request.form)
    wat.bust_handle_cache()
  return render_template('settings.html', settings=settings.get_all(), message=output['message'], message_class=output['class'])


# Serve Static Assets
@app.route('/assets/<path:filename>')
def send_assets(filename):
    return send_from_directory('assets', filename)


# It's Go Time
if __name__ == "__main__":
  network_settings = settings.get('network')
  app.run(host=network_settings[1], port=int(network_settings[2]))
