import json
import os
import shutil
from deps import find_dependencies
from helper import download_packages_with_name_and_version
import zipfile


def run(args=None):
    """
    """
    pkgs_requested = list()
    for item in args.install:
        name = item
        version = None
        if ":" in item:
            name, version = item.split(":")
        if version is not None: version = f'{version}'
        pkgs_requested.append((name, version))

    with open('apama_packages.json', 'r') as json_file:
        packageData = json.load(json_file)
        pkgs_requested.extend([(x['name'], x['version']) for x in packageData['dependencies']])

    packages_to_install = find_dependencies(pkgs_requested)

    packageData['dependencies'] = [{'name': k, 'version': v.to_str()} for (k, v) in packages_to_install.items()]

    with open('apama_packages.json', 'w') as json_file:
        json.dump(packageData, json_file, indent=2)

    runInstall(packages_to_install)


def add_arguments(parser):
    """
    """
    parser.add_argument(dest="install", nargs="*")


def runInstall(packages_to_install):
    os.makedirs('apama_packages', exist_ok=True)
    manifest_file = os.path.join('apama_packages', 'install.properties')
    already_installed = dict()
    if os.path.exists(manifest_file):
        with open(manifest_file, 'r') as fp:
            for l in fp:
                l = l.strip()
                if l.startswith('#') or len(l) == 0: continue
                t = l.split('=')
                already_installed[t[0]] = t[1]

    for (n, v) in packages_to_install.items():
        if n in already_installed:
            val = already_installed.pop(n)
            if val == v.to_str():
                if os.path.exists(os.path.join('apama_packages', n)):
                    # print(f'Package {n} with version {v.to_str()} already installed, doing nothing')
                    continue
            else:
                # Different version of the package is installed, so delete the existing one and perform the upgrade/downgrade
                if os.path.exists(os.path.join('apama_packages', n)):
                    shutil.rmtree(os.path.join('apama_packages', n))
        # Download the package
        tmpFile = os.path.join('apama_packages', n + '.zip')
        download_packages_with_name_and_version(n, v.to_str(), tmpFile)

        # Install the package
        z = zipfile.ZipFile(tmpFile)
        z.extractall(os.path.join('apama_packages', n))
        os.remove(tmpFile)

    # cleanup old dependencies
    if len(already_installed) > 0:
        for n in already_installed.keys():
            if os.path.exists(os.path.join('apama_packages', n)):
                shutil.rmtree(os.path.join('apama_packages', n))

    with open(manifest_file, 'w') as fp:
        fp.write('\n'.join(['%s=%s' % (k, v) for (k, v) in packages_to_install.items()]))
