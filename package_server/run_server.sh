#!/bin/bash
python3 -m venv package_server_venv

source package_server_venv/bin/activate

pip3 install -r requirements.txt

export PYTHONPATH=`pwd`
echo $PYTHONPATH

python3 app.py
