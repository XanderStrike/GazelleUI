# WhatUI
#   https://github.com/XanderStrike/WhatUI

import os
import sys
from datetime import timedelta

from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, Response, session, flash
from flask_apscheduler import APScheduler

from lib.auth import login_required, check_auth, needs_auth, api_key_required, get_or_create_api_key, regenerate_api_key
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
    PERMANENT_SESSION_LIFETIME = timedelta(days=365 * 10)  # 10 years

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

# Generate api key on first run
get_or_create_api_key()


def map_artist_results_for_api(results):
  groups = []

  for group in results.get('torrentgroup', []):
    mapped_torrents = []
    for t in group.get('torrent', []):
      mapped_torrents.append({
        'torrent_id': int(t.get('id')) if t.get('id') else None,
        'media': t.get('media'),
        'format': t.get('format'),
        'encoding': t.get('encoding'),
        'size': t.get('size'),
        'snatched': t.get('snatched'),
        'seeders': t.get('seeders'),
        'leechers': t.get('leechers'),
        'display_title': t.get('displayTitle'),
        'time': t.get('time'),
        'already_snatched': bool(t.get('alreadySnatched'))
      })

    groups.append({
      'group_id': int(group.get('groupId')) if group.get('groupId') else None,
      'group_name': group.get('groupName'),
      'group_year': group.get('groupYear'),
      'release_type': group.get('releaseType'),
      'torrents': mapped_torrents
    })

  return {
    'artist': {
      'id': int(results.get('id')) if results.get('id') else None,
      'name': results.get('name'),
      'image': results.get('image')
    },
    'groups': groups
  }


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
            session.permanent = True
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
  cred_setting = settings.get('what_credentials')
  auth_setting = settings.get('what_auth')
  if not auth_setting[1] and (not cred_setting[1] or not cred_setting[2]):
    return render_template('settings.html', settings=settings.get_all(), message="Please set your tracker's session cookie, or username and password.", message_class="alert-error")
  torrents = torrent.get_recent()
  return render_template('index.html', torrents=torrents, userinfo=database.userinfo(), settings=settings.get_all())

@app.route("/artist")
@login_required
def artist():
  query = request.args['q']
  results = wat.get_artist(query)
  return render_template('artist.html', results=results, userinfo=database.userinfo(), settings=settings.get_all(), mappings=autofetch.mappings)


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
    if request.form.get('setting') == 'api_key':
      output = {'class': 'alert-error', 'message': 'api key is read-only. use regenerate.'}
    else:
      output = settings.update(request.form)
      wat.bust_handle_cache()
  return render_template('settings.html', settings=settings.get_all(), message=output['message'], message_class=output['class'], userinfo=database.userinfo())


@app.route('/settings/regenerate_api_key', methods=['POST'])
@login_required
def regenerate_api_key_path():
  regenerate_api_key()
  flash('API Key Regenerated.', 'alert-success')
  return redirect('/settings')

@app.route("/snatches")
@login_required
def snatches():
  torrents = torrent.get_all()
  return render_template('snatches.html', torrents=torrents, userinfo=database.userinfo(), settings=settings.get_all())

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
  return render_template('subscriptions.html', subs=subs, userinfo=database.userinfo(), settings=settings.get_all(), mappings=autofetch.mappings)

@app.route('/refresh_userinfo')
@login_required
def refresh_userinfo():
  try:
    wat.refresh_user_info()
  except Exception as e:
    print('Failed to refresh user info: ' + str(e))

  return redirect(request.referrer or '/')

# api
@app.route('/api/v1/artists/search')
@api_key_required
def api_artist_search():
  query = request.args.get('q', '').strip()
  if not query:
    return jsonify({'error': 'missing query', 'details': {'q': 'required'}}), 400

  try:
    results = wat.get_artist(query)
  except Exception as e:
    return jsonify({'error': 'upstream failure', 'details': {'message': str(e)}}), 502

  if results == 'no data' or not results:
    return jsonify({'error': 'artist not found', 'details': {'q': query}}), 404

  payload = map_artist_results_for_api(results)
  payload['query'] = query
  return jsonify(payload)


@app.route('/api/v1/downloads', methods=['POST'])
@api_key_required
def api_download_create():
  data = request.get_json(silent=True) or {}

  required = ['torrent_id', 'artist', 'album', 'display_title', 'media', 'format', 'encoding']
  missing = [field for field in required if data.get(field) in [None, '']]
  if missing:
    return jsonify({'error': 'invalid request', 'details': {'missing': missing}}), 400

  torrent_id = str(data['torrent_id'])
  artist = str(data['artist'])
  album = str(data['album'])

  if torrent.exists(torrent_id, artist, album):
    return jsonify({'error': 'already queued', 'details': {'torrent_id': torrent_id}}), 409

  queue_data = {
    'id': torrent_id,
    'artist': artist,
    'album': album,
    'displayTitle': str(data['display_title']),
    'media': str(data['media']),
    'format': str(data['format']),
    'encoding': str(data['encoding'])
  }

  try:
    torrent.queue(queue_data)
  except Exception as e:
    return jsonify({'error': 'failed to queue download', 'details': {'message': str(e)}}), 500

  return jsonify({'status': 'queued', 'torrent_id': torrent_id}), 202


@app.route('/api/v1/downloads')
@api_key_required
def api_download_list():
  status = request.args.get('status')
  limit_raw = request.args.get('limit', '50')

  try:
    limit = int(limit_raw)
  except ValueError:
    return jsonify({'error': 'invalid request', 'details': {'limit': 'must be an integer'}}), 400

  if limit < 1:
    return jsonify({'error': 'invalid request', 'details': {'limit': 'must be >= 1'}}), 400

  if limit > 500:
    limit = 500

  if status not in [None, 'queued', 'downloaded']:
    return jsonify({'error': 'invalid request', 'details': {'status': 'must be queued or downloaded'}}), 400

  rows = torrent.get_all()
  items = []
  for row in rows:
    downloaded = bool(row['downloaded'])
    if status == 'queued' and downloaded:
      continue
    if status == 'downloaded' and not downloaded:
      continue

    items.append({
      'torrent_id': row['id'],
      'artist': row['artist'],
      'album': row['album'],
      'release': row['release'],
      'quality': row['quality'],
      'added': row['added'],
      'downloaded': downloaded
    })

    if len(items) >= limit:
      break

  return jsonify({'items': items})

# Support relative links from artist/album descriptions
@app.route('/artist.php')
@login_required
def artist_redirect():
  artistname = request.args.get('artistname')
  if artistname:
    return redirect(f'/artist?q={artistname}')
  return redirect('/')

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
