![](http://i.imgur.com/F8hk1Nv.png)

WhatUI is a web based torrent manager a-la CouchPotato, Headphones, or SickRage, but just for What.CD. It serves as a web wrapper for What's API, and downloads torrents into a folder that can be 'watched' by any torrent client for instant downloading.

It's minimal, it's fast, and it works on your phone. What more do you want.

[Check out these awesome screenshots](http://imgur.com/a/98KuP)

## Installation

WhatUI is designed with seedboxes in mind. These instructions are for Ubuntu, but it'll run on most any linux or osx box.

[Download the zip](https://github.com/XanderStrike/WhatUI/archive/master.zip) and extract it, or clone this repository.

Set up the prerequisites and run:

    sudo apt-get update
    sudo apt-get install wget python-pip
    sudo pip install flask whatapi
    python WhatUI.py


Then visit `<ip-address>:2020` to set it up!
