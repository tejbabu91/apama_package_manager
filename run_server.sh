#!/bin/bash
export PATH=/var/tmp/apama-lib4/linux/amd64/rhel7-gcc4.8.5/python/3.7.4:$PATH

python3 -m venv package_server_venv

source package_server_venv/bin/activate

pip install -r requirements.txt

export PYTHONPATH="."
python3 package_server/app.py
