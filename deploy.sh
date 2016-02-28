#!/bin/bash

cd /opt/dankbot
source .venv35/bin/activate
git pull
pip install --upgrade -e .
