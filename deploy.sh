#!/bin/bash

cd /opt/dankbot
source venv/bin/activate
git pull
pip install --upgrade -e .
