# Flask Starter
#   server.py
#   This file is the web server, it drives the application.

import sys
import os
from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, Response
import sqlite3 as lite
from datetime import datetime as time
import whatapi

from lib.auth import requires_auth

app = Flask(__name__)


# Settings

PORT = 2020
app.config.update(DEBUG=True)

try:
  apihandle = whatapi.WhatAPI(username='xanderstrike', password=os.environ['WHAT_PASSWORD'])
except whatapi.whatapi.LoginException:
  print "Username and password not set. Set them in server.py"
  sys.exit()


# Schema
#   Add table names as keys and column names as elements of an array
schema = {
  'visit':
    [
      "ip",
      "time"
    ]
}


# Initialize Database
#   Builds a database based on the schema provided, if none already exists
con = lite.connect('db.sqlite3')
try:
  con.cursor().execute("select * from " + schema.keys()[0])
except lite.OperationalError:
  print "No DB found, creating..."
  for k in schema.keys():
    con.cursor().execute("create table " + k + "(" + ", ".join(schema[k]) + ");")


# Methods
#   The methods you use in your app
def get_time():
  return str(time.now())

def record_visit(request):
  con = lite.connect('db.sqlite3')
  command = "insert into visit values('%s', '%s')" % (request.host, get_time())
  con.cursor().execute(command)
  con.commit()
  return True

def get_visits():
  cur = lite.connect('db.sqlite3').cursor()
  return cur.execute('select count(1) from visit').fetchall()[0][0]

def get_artist_results(query):
  try:
    return apihandle.request('artist', artistname=query)['response']
  except whatapi.whatapi.RequestException:
    return "an error"

def get_torrent_results(torrent_id):
  # try:
  return apihandle.request('torrent', id=torrent_id)['response']
  # except whatapi.whatapi.RequestException:
    # return "an error"

# Routes
#   The actual routes you can visit in your app
@app.route("/")
@requires_auth
def index():
  record_visit(request)
  return render_template('index.html')

@app.route("/search")
@requires_auth
def search():
  record_visit(request)
  query = request.args['q']
  results = get_artist_results(query)
  return render_template('search.html', results=results)

@app.route("/want")
@requires_auth
def want():
  torrent_id = request.args['id']
  download_link = 'https://ssl.what.cd/torrents.php?action=download&id=' + torrent_id + '&authkey=' + apihandle.authkey + '&torrent_pass=' + apihandle.passkey
  os.system("wget \"" + download_link + "\" -O " + torrent_id + ".torrent")
  return "ok"

@app.route("/torrent")
@requires_auth
def torrent():
  torrent_id = request.args['id']
  results = get_torrent_results(torrent_id)
  download_link = 'https://ssl.what.cd/torrents.php?action=download&id=' + torrent_id + '&authkey=' + apihandle.authkey + '&torrent_pass=' + apihandle.passkey
  return render_template('torrent.html', torrent=results, link=download_link)

# Serve Static Assets
#   Drop any assets (images, js, css) into the assets folder or subfolders and voila
@app.route('/assets/<path:filename>')
def send_assets(filename):
    return send_from_directory('assets', filename)


# It's Go Time
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=PORT)
