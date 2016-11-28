# Rest in peace What.cd

I'm absolutely crushed. What.cd was the most complete repository of our musical history that has ever existed. I hope we can achieve something like that again.

Unfortunately, this project is no longer functional. I _suspect_ it will work with other sites running Gazelle, but I can't be certain. I fully intend to update this, or build a new app that works with whatever comes next, as soon as I get an invitation (my email's in my profile wink wink).

![](http://i.imgur.com/NNByEC0.png)

WhatUI is a web based torrent manager a-la CouchPotato, Headphones, or SickRage, but just for What.CD. It serves as a web wrapper for What's API, and downloads torrents into a folder that can be 'watched' by any torrent client for instant downloading.

It's minimal, it's fast, and it works on your phone. What more do you want.

[Check out these awesome screenshots](http://imgur.com/a/98KuP)

## Installation

WhatUI is designed with seedboxes in mind. These instructions are for Ubuntu, but it'll run on most any linux or osx box.

[Download the zip](https://github.com/XanderStrike/WhatUI/archive/master.zip) and extract it, or clone this repository.

Set up the prerequisites and run:

    sudo apt-get update
    sudo apt-get install wget python-pip
    sudo pip install flask flask_apscheduler whatapi
    python WhatUI.py


Then visit `<ip-address>:2020` to set it up!
