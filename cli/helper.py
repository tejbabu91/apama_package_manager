import urllib.request
import os
import json
from model import *
SERVER_URL = os.environ.get('SERVER_URL', 'http://localhost:5000')

if not SERVER_URL.endswith('/'): SERVER_URL = SERVER_URL + '/'

PACKAGES_PATH = SERVER_URL + 'packages'

packages_info_cache: Dict[str, Dict[Version, Package]] = {}

def sort_pkg_by_versions(packages: List[Package]) -> List[Package]:
    return sorted(packages, key=lambda x: Version.from_str(x.version))

def get_all_packages():
    req = urllib.request.Request(url=PACKAGES_PATH, method='GET')
    resp = urllib.request.urlopen(req)
    if resp.status != 200:
        raise Exception(f'Received code : {resp.status}, reason : {resp.reason}, body : {resp.read().decode("utf-8")}')

    result = json.loads(resp.read().decode('utf-8'))['packages']
    result = [Package.from_dict(i) for i in result]

    # cache the result for later package specific calls
    for p in result:
        versions = packages_info_cache.setdefault(p.name)
        versions[Version.from_str(p.version)] = p

    return result

def get_all_packages_with_name(name):
    if name in packages_info_cache:
        versions = packages_info_cache[name].values()
        return sort_pkg_by_versions(versions)

    req = urllib.request.Request(url=PACKAGES_PATH + '/' + name, method='GET')
    resp = urllib.request.urlopen(req)

    if resp.status == 404:
        return list()

    if resp.status != 200:
        raise Exception(f'Received code : {resp.status}, reason : {resp.reason}, body : {resp.read().decode("utf-8")}')

    result = json.loads(resp.read().decode('utf-8'))['packages']
    result = sort_pkg_by_versions([Package.from_dict(i) for i in result])

    d = {}
    for p in result:
        d[Version.from_str(p.version)] = p
    packages_info_cache[name] = d
    return result

def get_all_package_versions(name: str) -> List[Version]:
    pkgs = get_all_packages_with_name(name)
    return [Version.from_str(p.version) for p in pkgs]

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

if __name__ == '__main__':
    print(get_all_packages_with_name('empty_package'))