import urllib.request
import os
import json

SERVER_URL = os.environ.get('SERVER_URL', 'http://localhost:5000')

if not SERVER_URL.endswith('/'): SERVER_URL = SERVER_URL + '/'

PACKAGES_PATH = SERVER_URL + 'packages'

def get_all_packages():
    req = urllib.request.Request(url=PACKAGES_PATH, method='GET')
    resp = urllib.request.urlopen(req)
    if resp.status != 200:
        raise Exception(f'Received code : {resp.status}, reason : {resp.reason}, body : {resp.read().decode("utf-8")}')

    return json.loads(resp.read().decode('utf-8'))['packages']

def get_all_packages_with_name(name):
    req = urllib.request.Request(url=PACKAGES_PATH + '/' + name, method='GET')
    resp = urllib.request.urlopen(req)

    if resp.status == 404:
        return list()

    if resp.status != 200:
        raise Exception(f'Received code : {resp.status}, reason : {resp.reason}, body : {resp.read().decode("utf-8")}')

    return json.loads(resp.read().decode('utf-8'))['packages']

def download_packages_with_name_and_version(name, version, targetPath):
    urllib.request.urlretrieve(PACKAGES_PATH + '/' + name + '/' + version, filename=targetPath)

def upload_package(filePath):
    data = None
    with open(filePath, 'rb') as f:
        data = f.read()
    req = urllib.request.Request(url=PACKAGES_PATH, data=data, method='POST')
    resp = urllib.request.urlopen(req)

    if resp.status != 201:
        raise Exception(f'Received code : {resp.status}, reason : {resp.reason}, body : {resp.read().decode("utf-8")}')
