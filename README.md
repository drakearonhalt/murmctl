## murmctl

Command line administration for Murmur (mumble-server).

* * *
Requirements:

* Murmur Static Linux 1.2.5

* Python 2.6.6

* LibICE

* Python ICE bindings

* argparse from CentOS repo

Developed on CentOS 6.5
murmctl may work with other versions but has not been tested.

* * *

Currently supports the following:
* listing server data: channels, usernames
* show status
* display logs to screen
* kick users by name
* send a message to a user
* adding and removing channels

* * * 
Installation

git clone https://github.com/drakearonhalt/murmctl.git
cd murmctl
./murmctl.py -h

* right now the Murmur.ice file is hardcoded to /opt/murmur this may need to be changed for your installation.
