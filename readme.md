![](https://i.imgur.com/rRBAXAU.png)

GazelleUI is a web based torrent manager for music, like Lidarr, specifically for Gazelle based music trackers (such as ~~WhatCD~~, ~~APL~~, ~~PTH~~, RED). 

It is simply a wrapper for your tracker's API. Search for an artist or album, snatch your preferred quality, and the torrent will be downloaded to a watchfolder.

It's minimal, it's fast, and it works on your phone. What more do you want.

[Check out these awesome screenshots](https://imgur.com/a/fZysf)

## Installation

Docker/podman compose is the recommended way to run GazelleUI.

```yaml
services:
  gazelleui:
    image: xanderstrike/gazelleui
    ports:
      - "2020:2020"
    volumes:
      - ./config:/app/config
      - ./torrents:/torrents
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    depends_on:
      - transmission
```

* Set the watchfolder to a directory watched by your torrent client
* PGID and PUID can be found by running `id` in a terminal
* Timezone is your timezone
* Configure the port by setting `2020:2020` to `<your port>:2020`

See [docker-compose.yml](docker-compose.yml) for an example running with a companion transmission.

### Without Docker or for Development

GazelleUI is designed with seedboxes in mind. These instructions are for Ubuntu, but it'll run on most any linux or osx box.

Download or clone this repository.

Set up the prerequisites and run:

    sudo apt-get update
    sudo apt-get install wget python3-pip
    sudo pip install -r requirements.txt
    python GazelleUI.py

Then visit `<ip-address>:2020` to set it up!

### License

MIT license

Logo credit Focus Lab via NounProject: https://thenounproject.com/search/?q=gazelle&i=549876
