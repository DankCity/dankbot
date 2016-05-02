# Dankbot

[![Circle CI](https://circleci.com/gh/DankCity/dankbot/tree/master.svg?style=svg)](https://circleci.com/gh/DankCity/dankbot/tree/master) [![Coverage Status](https://coveralls.io/repos/github/DankCity/dankbot/badge.svg?branch=master)](https://coveralls.io/github/DankCity/dankbot?branch=master) [![Code Health](https://landscape.io/github/DankCity/dankbot/master/landscape.svg?style=flat)](https://landscape.io/github/DankCity/dankbot/master) [![Stories in Ready](https://badge.waffle.io/DankCity/dankbot.svg?label=ready&title=Ready)](http://waffle.io/DankCity/dankbot)

A Slack Bot that scrapes memes from subreddits and posts them to slack

## Steps to run

### Clone into directory
```
cd /opt
sudo mkdir dankbot && sudo chown <user>:<user> dankbot
git clone git@github.com:DankCity/dankbot.git
```

### Setup INI file
```
cd /opt/dankbot
cp dankbot/dankbot.ini.sample dankbot/dankbot.ini
```

Edit the INI file to fill in the missing token, username, and password fields:
```
(.venv35)➜  dankbot git:(master) ✗ cat dankbot/dankbot.ini.sample
[slack]
token: <put here>
channel: #random

[reddit]
subreddits: dankmemes, fishpost, me_irl, 4chan

[imgur]
client_id: <client_id>
client_secret: <client Secret>

[mysql]
database: <db>
username: <username>
password: <password>

[misc]
include_nsfw: <boolean>
max_memes: 3
```

### Create and activate a virtual environment
```
cd /opt/dankbot
virtualenv --python=`which python3` env
source env/bin/activate
```

### Install the python package
```
cd /opt/dankbot
source env/bin/activate
pip install -e .
```

### Create logging folder
```
sudo mkdir /var/log/dankbot
sudo chown <user> /var/log/dankbot
```

### Add an entry to your crontab:
Edit the crontab with your favorite editor
```
sudo vi /etc/crontab
```
And add an entry like so:
```
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the 'crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow usernamecommand
*/5 09-17 * * 1-5 root cd /opt/dankbot && source env/bin/activate && dankbot .
```

This will run dankbot once every 5 minutes, Monday to Friday, between 9 AM and
5 PM CST
