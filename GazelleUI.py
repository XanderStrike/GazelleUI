# WhatUI
#   https://github.com/XanderStrike/WhatUI

import os
import sys

from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, Response, session
from flask_apscheduler import APScheduler

from lib.auth import login_required, check_auth, needs_auth
import lib.database as database
import lib.settings as settings
import lib.wat as wat
import lib.jobs as jobs
import lib.torrent as torrent
import lib.autofetch as autofetch

import json

# Configure Scheduler
class Config(object):
    JOBS = jobs.job_list()
    SCHEDULER_VIEWS_ENABLED = True
    SCHEDULER_TIMEZONE = "America/Los_Angeles"
    DEBUG = True

app = Flask(__name__)
app.config.from_object(Config())

# Make session available in all templates
@app.context_processor
def inject_session():
    return dict(session=session)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Initialize Database
database.init()

# Generate or retrieve secret key from database
def get_or_create_secret_key():
    try:
        result = settings.get('secret_key')
        if result and result[1]:
            return result[1].encode('utf-8')
    except:
        pass

    secret_key = os.urandom(24).hex()
    settings.update({'setting': 'secret_key', 'value_1': secret_key, 'value_2': ''})
    return secret_key.encode('utf-8')

app.secret_key = get_or_create_secret_key()

# Routes
@app.route("/login", methods=['GET', 'POST'])
def login():
    if not needs_auth():
        return redirect('/')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if check_auth(username, password):
            session['logged_in'] = True
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

@app.route("/")
@login_required
def index():
  setting = settings.get('what_credentials')
  if setting[1] == None or setting[1] == '':
    return render_template('settings.html', settings=settings.get_all(), message="Please set your whatcd username and password.", message_class="alert-error")
  torrents = torrent.get_recent()
  return render_template('index.html', torrents=torrents, userinfo=database.userinfo())

@app.route("/artist")
@login_required
def artist():
  query = request.args['q']
  results = wat.get_artist(query)
  return render_template('artist.html', results=results, userinfo=database.userinfo())


@app.route("/want", methods=['POST'])
@login_required
def want():
  torrent.queue(json.loads(request.form['data']))
  return "<button class='button' disabled>Snatched!</button>"

@app.route("/group_info")
@login_required
def group_info():
  group_id = request.args['id']
  results = wat.get_group(group_id)
  return render_template('group_info.html', group_info=results)

@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings_path():
  output = {'message':None,'class':None}
  if request.method == 'POST':
    output = settings.update(request.form)
    wat.bust_handle_cache()
  return render_template('settings.html', settings=settings.get_all(), message=output['message'], message_class=output['class'], userinfo=database.userinfo())

@app.route("/snatches")
@login_required
def snatches():
  torrents = torrent.get_all()
  return render_template('snatches.html', torrents=torrents, userinfo=database.userinfo())

@app.route('/delete_sub/<int:sub_id>')
@login_required
def delete_sub(sub_id):
  database.delete_sub(sub_id)
  return redirect('/subscriptions')

@app.route('/create_sub', methods=['POST'])
@login_required
def create_sub():
  autofetch.create_subscription(request.form)
  return redirect('/subscriptions')

@app.route("/subscriptions")
@login_required
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
  app.run(host=network_settings[1], port=int(network_settings[2]), use_reloader=False, debug=False)
