# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GazelleUI is a web-based torrent manager for music, specifically designed for Gazelle-based music trackers (RED, formerly WhatCD/APL/PTH). It acts as a wrapper for tracker APIs, allowing users to search for artists/albums and automatically download torrents to a watch folder.

## Development Commands

**Run locally (development):**
```bash
pip install -r requirements.txt
python GazelleUI.py
```

**Run with Docker/Podman (recommended):**
```bash
podman-compose up -d  # or docker-compose up -d
```

**Build the container image:**
```bash
podman build -t gazelleui .  # or docker build
```

**Production (via Gunicorn):**
```bash
gunicorn -w 1 -b 0.0.0.0:2020 wsgi:app
```

The application runs on port 2020 by default.

## Architecture

### Application Structure

- **`GazelleUI.py`** - Main Flask application entry point with all routes
- **`wsgi.py`** - WSGI entry point for production (Gunicorn)
- **`lib/`** - Core business logic modules
- **`templates/`** - Jinja2 HTML templates
- **`assets/`** - Static assets (CSS, JS, images)
- **`config/`** - SQLite database and configuration (volume-mounted in container)
- **`lib/whatapi/`** - Gazelle tracker API wrapper

### Core Library Modules (`lib/`)

- **`wat.py`** - Primary API integration layer. Handles Gazelle tracker API calls (artist search, torrent groups, download links) with 24-hour response caching. Uses `whatapi.WhatAPI` for authentication.
- **`database.py`** - SQLite3 operations. Schema defined in `SCHEMA` dict with auto-migration on init. Tables: `settings`, `torrents`, `user`, `subscriptions`. Database file: `config/data.sqlite3`
- **`settings.py`** - Configuration management stored in database key-value pairs
- **`torrent.py`** - Torrent download queue management and file operations
- **`autofetch.py`** - Subscription-based auto-fetching system with release type mappings (Album, EP, Compilation, etc.)
- **`jobs.py`** - Scheduled task definitions for APScheduler
- **`auth.py`** - Session-based authentication (username/password)

### Scheduled Jobs (APScheduler)

Jobs are defined in `lib/jobs.py` and run on interval:
- **torrents** (10s) - Downloads queued torrents
- **update_user_info** (900s/15min) - Refreshes user stats from tracker
- **autofetch** (11520s/3.2hr) - Runs subscription-based searches

### Authentication Flow

Two auth methods supported:
1. **Session cookie** - Stored in `what_auth` setting (preferred)
2. **Username/password** - Stored in `what_credentials` setting

The app can also have its own web UI credentials (`webui_credentials` setting).

### API Integration

Uses the Gazelle AJAX API via `lib/whatapi/whatapi.py`:
- Artist search: `action=artist`
- Torrent group: `action=torrentgroup`
- Index (user info): `action=index`
- Downloads: Direct torrent URL with authkey/passkey

Domain is configurable via the `domain` setting (default: `https://redacted.sh`).

### Release Type Mappings

Gazelle tracker release types are mapped in `lib/autofetch.py` as an Enum (Album=1, Soundtrack=3, EP=5, etc.). These correspond to tracker API values.

### Configuration Notes

- Settings are stored in SQLite, not files
- The `secret_key` for Flask sessions is auto-generated on first run and stored in database
- Volume mounts: `./config:/app/config` and `./torrents:/torrents`
- Torrent watch folder path: `/torrents/` (configurable via `torrent` setting)
- Token usage: Can use freeleech tokens if enabled in settings
