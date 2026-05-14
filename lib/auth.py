from flask import request, jsonify, session, redirect
from functools import wraps
import secrets
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


def get_or_create_api_key():
    current = settings.get('api_key')[1]
    if current:
        return current

    return regenerate_api_key()


def regenerate_api_key():
    api_key = secrets.token_urlsafe(32)
    settings.update({'setting': 'api_key', 'value_1': api_key, 'value_2': ''})
    return api_key


def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        header = request.headers.get('Authorization', '')
        parts = header.split(' ', 1)

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'unauthorized'}), 401

        token = parts[1].strip()
        if not token or token != get_or_create_api_key():
            return jsonify({'error': 'unauthorized'}), 401

        return f(*args, **kwargs)

    return decorated
