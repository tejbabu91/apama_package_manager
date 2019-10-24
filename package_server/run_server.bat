python -m venv package_server_venv

call package_server_venv/bin/activate

pip install -r requirements.txt

set PYTHONPATH=`pwd`

python app.py
