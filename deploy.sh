#!/bin/bash

cd /opt/dankbot
source env/bin/activate
git pull
pip install --upgrade -e .
