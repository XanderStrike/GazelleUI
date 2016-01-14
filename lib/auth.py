# Original: http://flask.pocoo.org/snippets/8/

from flask import request, Response
from functools import wraps
import lib.settings as settings

def check_auth(username, password):
    creds = settings.get('webui_credentials')
    return username == creds[1] and password == creds[2]

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not needs_auth() and (not auth or not check_auth(auth.username, auth.password)):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def needs_auth():
    creds = settings.get('webui_credentials')
    return creds[1] == None or creds[1] == ''
