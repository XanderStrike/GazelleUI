![](https://i.imgur.com/rRBAXAU.png)

GazelleUI is a web based torrent manager a-la CouchPotato, Headphones, or SickRage, but just for [Gazelle](https://github.com/WhatCD/Gazelle) based music trackers (such as APL or PTH). It serves as a web wrapper for Gazelle's API, and downloads torrents into a folder that can be 'watched' by any torrent client for instant downloading.

It's minimal, it's fast, and it works on your phone. What more do you want.

[Check out these awesome screenshots](https://imgur.com/a/fZysf)

## Installation

If you've got it, [Docker](https://www.docker.com/) is the best way to run GazelleUI.

    docker create \
      --name=gazelleui \
      --restart always \
      -v <path to watchfolder>:/torrents \
      -e PGID=1000 -e PUID=1000  \
      -e TZ=America/Los_Angeles \
      -p 2020:2020 \
      xanderstrike/gazelleui

* Set the watchfolder to a directory watched by your torrent client
* PGID and PUID can be found by running `id` in a terminal
* Timezone is your timezone
* Configure the port by setting `2020:2020` to `<your port>:2020`

Run with:

    docker start gazelleui

### Without Docker or for Development

GazelleUI is designed with seedboxes in mind. These instructions are for Ubuntu, but it'll run on most any linux or osx box.

Download or clone this repository.

Set up the prerequisites and run:

    sudo apt-get update
    sudo apt-get install wget python-pip
    sudo pip install -r requirements.txt
    python GazelleUI.py


Then visit `<ip-address>:2020` to set it up!

### License

MIT license

Logo credit Focus Lab via NounProject: https://thenounproject.com/search/?q=gazelle&i=549876
