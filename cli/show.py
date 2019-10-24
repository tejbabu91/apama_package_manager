from helper import get_all_packages, get_all_packages_with_name
from model import *

def run(args=None):
	"""
	list of packages
	"""
	packages_to_display = args.show
	metadata = dict()
	for package in get_all_packages():
		if package.name in packages_to_display:
			metadata[package.name] = True

	for name in metadata.keys():
		versions = get_all_packages_with_name(name)
		print(f'\n\tName = {name}')
		print(f'\tDescription = {versions[0].description}')
		print(f'\tLatest Version = {versions[0].version}')
		print(f'\tDependencies = {", ".join([x.name for x in versions[0].dependencies]) if len(versions[0].dependencies) > 0 else None}')
		print(f'\tAlternative Versions = {", ".join([x.version for x in versions[1:]]) if len(versions) > 1 else None}')

	print('')
	for (i, n) in enumerate(packages_to_display):
		if n not in metadata:
			print(f'\tPackage "{n}" not found !!!')

def add_arguments(parser):
	"""
	"""
	parser.add_argument(dest="show", nargs="+")
