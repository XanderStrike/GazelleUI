# WhatUI
#   https://github.com/XanderStrike/WhatUI

import os
import sys

from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, Response
from flask_apscheduler import APScheduler

from lib.auth import requires_auth
import lib.database as database
import lib.settings as settings
import lib.wat as wat
import lib.jobs as jobs
import lib.torrent as torrent
import lib.autofetch as autofetch

import json

# import logging
# logging.basicConfig()

# Configure Scheduler
class Config(object):
    JOBS = jobs.job_list()
    SCHEDULER_VIEWS_ENABLED = True
    SCHEDULER_TIMEZONE = "America/Los_Angeles"
    DEBUG = True

app = Flask(__name__)
app.config.from_object(Config())

if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
  scheduler = APScheduler()
  scheduler.init_app(app)
  scheduler.start()


# Initialize Database
database.init()


# Routes
@app.route("/")
@requires_auth
def index():
  setting = settings.get('what_credentials')
  if setting[1] == None or setting[1] == '':
    return render_template('settings.html', settings=settings.get_all(), message="Please set your whatcd username and password.", message_class="alert-error")
  torrents = torrent.get_recent()
  return render_template('index.html', torrents=torrents, userinfo=database.userinfo())

@app.route("/artist")
@requires_auth
def artist():
  query = request.args['q']
  results = wat.get_artist(query)
  return render_template('artist.html', results=results, userinfo=database.userinfo())

@app.route("/browse")
@requires_auth
def browse():
  query = request.args['q']
  results = wat.browse(query)
  return render_template('browse.html', results=results, query=query, userinfo=database.userinfo())

@app.route("/label")
@requires_auth
def label():
  query = request.args['q']
  results = wat.label(query)
  return render_template('browse.html', results=results, query=query, userinfo=database.userinfo())

@app.route("/want", methods=['POST'])
@requires_auth
def want():
  torrent.queue(json.loads(request.form['data']))
  return "<button class='button' disabled>Snatched!</button>"

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
  return render_template('settings.html', settings=settings.get_all(), message=output['message'], message_class=output['class'], userinfo=database.userinfo())

@app.route("/snatches")
@requires_auth
def snatches():
  torrents = torrent.get_all()
  return render_template('snatches.html', torrents=torrents, userinfo=database.userinfo())

@app.route('/delete_sub/<int:sub_id>')
@requires_auth
def delete_sub(sub_id):
  database.delete_sub(sub_id)
  return redirect('/subscriptions')

@app.route('/create_sub', methods=['POST'])
@requires_auth
def create_sub():
  autofetch.create_subscription(request.form)
  return redirect('/subscriptions')

@app.route("/subscriptions")
@requires_auth
def subscriptions():
  subs = database.subscriptions()
  return render_template('subscriptions.html', subs=subs, userinfo=database.userinfo())

# Serve Static Assets
@app.route('/assets/<path:filename>')
def send_assets(filename):
  return send_from_directory('assets', filename)

@app.route('/<path:filename>')
def catch_all(filename):
  return send_from_directory('assets', filename)

# It's Go Time
if __name__ == "__main__":
  network_settings = settings.get('network')
  app.run(host=network_settings[1], port=int(network_settings[2]))
