from flask import Flask, request, send_file, Response
import os
import io
import json
from dataclasses import asdict

from manager import Manager

app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/packages', methods=['GET'])
def packages():
    return app.manager.get_manifest_json()

@app.route('/packages', methods=['POST'])
def packages_post():
    tmpfilepath = os.path.join(app.config['PACKAGE_DIR'], f'p_tmp.zip')
    with open(tmpfilepath, 'wb') as f:
        f.write(request.stream.read())

    app.manager.add_package(tmpfilepath)
    return Response(status=200)

@app.route('/packages/<name>', methods=['GET'])
def packages_name(name):
    return {"packages": list(map(lambda x: asdict(x), app.manager.get_package_manifests_by_name(name)))}

@app.route('/packages/<name>/<version>', methods=['GET'])
def packages_name_version(name, version):
    m = app.manager.get_package_manifest(name, version)
    with open(app.manager.get_package_path(m), 'rb') as f:
        return send_file(io.BytesIO(f.read()),
                         attachment_filename=f'{name}.{version}.zip',
                         mimetype='application/octet-stream')

if __name__ == '__main__':
    print(app.config)
    app.manager = Manager(app.config['PACKAGE_DIR'])
    app.run()

