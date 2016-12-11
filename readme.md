![](http://i.imgur.com/reN909I.png)

ApolloUI is a web based torrent manager a-la CouchPotato, Headphones, or SickRage, but just for Apollo.rip. It serves as a web wrapper for Apollo's API, and downloads torrents into a folder that can be 'watched' by any torrent client for instant downloading.

It's minimal, it's fast, and it works on your phone. What more do you want.

[Check out these awesome screenshots](http://imgur.com/a/98KuP)

## Installation

ApolloUI is designed with seedboxes in mind. These instructions are for Ubuntu, but it'll run on most any linux or osx box.

Download or clone this repository.

Set up the prerequisites and run:

    sudo apt-get update
    sudo apt-get install wget python-pip
    sudo pip install -r requirements.txt
    python ApolloUI.py


Then visit `<ip-address>:2020` to set it up!
