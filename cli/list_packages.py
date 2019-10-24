from cli.helper import get_all_packages

def run(args=None):
	"""
	list of packages
	"""
	print('')
	print('showing list of packages:')
	print('')
	for p in sorted(list(set([x['name'] for x in get_all_packages()]))):
		print(f'\t{p}')
	print('')

if __name__ == '__main__':
	run()