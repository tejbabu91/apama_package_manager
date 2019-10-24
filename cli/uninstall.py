import json

from deps import find_dependencies
from install import runInstall


def run(args=None):
    """
    """
    existingPackages = dict()
    with open('apama_packages.json', 'r') as json_file:
        packageData = json.load(json_file)
        for k in packageData['dependencies']:
            existingPackages[k['name']] = k['version']

    pkgs_to_be_uninstalled = list()
    for item in args.uninstall:
        name = item
        version = None
        if ":" in item:
            name, version = item.split(":")
        if name not in existingPackages:
            print(f'Package {name} not installed, doing nothing')
            continue
        if version is not None and existingPackages[name] != version:
            print(f'Package {name} with version {version} is not installed, Installed version is {existingPackages[name]}')
            continue
        existingPackages.pop(name)
        pkgs_to_be_uninstalled.append(name)

    # Get the dependencies for the remaining packages
    resolvedPackages = find_dependencies(existingPackages.items())

    for k in resolvedPackages.keys():
        if k in pkgs_to_be_uninstalled:
            print(f'Can\t uninstall {k} as other packages are dependent on it')

    packageData['dependencies'] = [{'name': k, 'version': v.to_str()} for (k, v) in resolvedPackages.items()]

    with open('apama_packages.json', 'w') as json_file:
        json.dump(packageData, json_file, indent=2)

    runInstall(resolvedPackages)


def add_arguments(parser):
    """
    """
    parser.add_argument(dest="uninstall", nargs="+")
