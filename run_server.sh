#!/bin/bash

python3 -m venv ~/package_server_venv

source ~/package_server_venv/bin/activate

pip3 install -r requirements.txt

export PYTHONPATH="."
python3 package_server/app.py
