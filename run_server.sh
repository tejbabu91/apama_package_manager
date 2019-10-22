#!/bin/bash

python -m venv ~/package_server_venv

source ~/package_server_venv/bin/activate

pip install -r requirements.txt

export PYTHONPATH="."
python package_server/app.py
