from flask import request, Response, session, redirect, url_for, render_template
from functools import wraps
import lib.settings as settings

def check_auth(username, password):
    creds = settings.get('webui_credentials')
    return username == creds[1] and password == creds[2]

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not needs_auth():
            return f(*args, **kwargs)
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

def needs_auth():
    creds = settings.get('webui_credentials')
    return creds[1] != None and creds[1] != ''
