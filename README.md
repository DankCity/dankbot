# Dankbot

[![Circle CI](https://circleci.com/gh/levi-rs/dankbot/tree/master.svg?style=svg)](https://circleci.com/gh/levi-rs/dankbot/tree/master) [![Coverage Status](https://coveralls.io/repos/github/levi-rs/dankbot/badge.svg?branch=master)](https://coveralls.io/github/levi-rs/dankbot?branch=master) [![Code Health](https://landscape.io/github/levi-rs/dankbot/master/landscape.svg?style=flat)](https://landscape.io/github/levi-rs/dankbot/master) [![Stories in Ready](https://badge.waffle.io/levi-rs/dankbot.svg?label=ready&title=Ready)](http://waffle.io/levi-rs/dankbot)

A Slack Bot that scrapes memes from subreddits and posts them to slack

## Steps to run

### Clone into directory
```
cd /opt
sudo mkdir dankbot && sudo chown <user>:<user> dankbot
git clone git@github.com:levi-rs/dankbot.git
```

### Setup INI file
```
cd /opt/dankbot
cp dankbot/dankbot.ini.sample dankbot/dankbot.ini
```

Edit the INI file to fillin the missing token, username, and password fields:
```
(.venv35)➜  dankbot git:(master) ✗ cat dankbot/dankbot.ini.sample
[slack]
token: <put here>
channel: #random

[reddit]
subreddits: dankmemes, fishpost

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
17 *17* * *17root    cd / && run-parts --report /etc/cron.hourly
25 6* * *25roottest -x /usr/sbin/anacron || ( cd / && run-parts --report
/etc/cron.daily )
47 6* * 7roottest -x /usr/sbin/anacron || ( cd / && run-parts --report
/etc/cron.weekly )
52 61 * *61roottest -x /usr/sbin/anacron || ( cd / && run-parts --report
/etc/cron.monthly )
#
*/5 10-18 * * 1-5 root cd /opt/dankbot && source env/bin/activate && dankbot .
```

This will run dankbot once every 5 minutes, Monday to Friday, between 9 AM and
5 PM CST
