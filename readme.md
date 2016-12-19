![](http://i.imgur.com/LWfT3y6.png)

GazelleUI is a web based torrent manager a-la CouchPotato, Headphones, or SickRage, but just for [Gazelle](https://github.com/WhatCD/Gazelle) based music trackers (such as APL or PTH). It serves as a web wrapper for Gazelle's API, and downloads torrents into a folder that can be 'watched' by any torrent client for instant downloading.

It's minimal, it's fast, and it works on your phone. What more do you want.

[Check out these awesome screenshots](http://imgur.com/a/98KuP)

## Installation

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