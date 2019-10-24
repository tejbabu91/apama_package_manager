import json
from model import *
from deps import find_dependencies

def run(args=None):
	"""
	"""
	pkgs_requested = dict()
	for item in args.install:
		name=item
		version=None
		if ":" in item:
			name, version = item.split(":")
		pkgs_requested[name] = version

	existingPackages = dict()
	packageData = None
	with open('apama_packages.json', 'r') as json_file:
		packageData = json.load(json_file)
		for k in packageData['dependencies']:
			existingPackages[k['name']] = k['version']

	for k in pkgs_requested.keys():
		if k in existingPackages: print(f'Package {k} already installed')

	existingPackages.update(pkgs_requested)

	packages_to_install = find_dependencies(existingPackages.items())

	packageData['dependencies'] = [{'name': k, 'version': v.to_str()} for (k,v) in packages_to_install.items()]

	with open('apama_packages.json', 'w') as json_file:
		json.dump(packageData, json_file, indent=2)

def add_arguments(parser):
	"""
	"""
	parser.add_argument(dest="install", nargs="*")
