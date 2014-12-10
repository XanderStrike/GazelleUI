# Flask Starter
#   server.py
#   This file is the web server, it drives the application.

from flask import Flask, request, jsonify, render_template, redirect, send_from_directory, Response, request
import sqlite3 as lite
from datetime import datetime as time

app = Flask(__name__)


# Settings
#   Any handy user modifyable variables ought to go here
PORT = 2020
app.config.update(DEBUG=True)


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


# Routes
#   The actual routes you can visit in your app
@app.route("/")
def index():
  record_visit(request)
  return render_template('index.html', time=get_time(), visits=get_visits())


# Serve Static Assets
#   Drop any assets (images, js, css) into the assets folder or subfolders and voila
@app.route('/assets/<path:filename>')
def send_assets(filename):
    return send_from_directory('assets', filename)


# It's Go Time
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=PORT)
