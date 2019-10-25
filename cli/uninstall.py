import json

from deps import find_dependencies
from install import runInstall

def run(args=None):
    """
    """
    existingPackages = dict()
    idx_to_delete = list()
    with open('apama_packages.json', 'r') as json_file:
        packageData = json.load(json_file)
        for (i,k) in enumerate(packageData['dependencies']):
            name = k['name']
            version = k['version']
            if name in args.uninstall:
                idx_to_delete.append(i)
            else:
                existingPackages[name] = k[version]

    if len(idx_to_delete) > 0:
        for i in reversed(idx_to_delete):
            del packageData['dependencies'][i]

    # Get the dependencies for the remaining packages
    resolvedPackages = find_dependencies(list(existingPackages.items()))

    for k in resolvedPackages.keys():
        if k in args.uninstall:
            print(f'Can\'t uninstall {k} as other packages are dependent on it')

    with open('apama_packages.json', 'w') as json_file:
        json.dump(packageData, json_file, indent=2)

    runInstall(resolvedPackages)

def add_arguments(parser):
    """
    """
    parser.add_argument(dest="uninstall", nargs="*")
