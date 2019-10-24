from helper import get_all_packages

def run(args=None):
	"""
	list of packages
	"""
	packages_to_display = args.show
	metadata = dict()
	for package in get_all_packages():
		if package['name'] in packages_to_display:
			if package['name'] not in metadata: metadata[package['name']] = list()
			metadata[package['name']].append(package)

	for (i, n) in enumerate(packages_to_display):
		if n not in metadata:
			print(f'Package {n} not found!!!\n')

def add_arguments(parser):
	"""
	"""
	parser.add_argument(dest="show", nargs="+")
