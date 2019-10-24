import urllib.request

def run(args=None):
	"""
	"""
	pkgs_list = []
	if args.install is not None:
		for item in args.install:
			name=item
			version=None
			if ":" in item:
				t = item.split(":")
				name, version = t[0], t[1]

			d = {"name":name, "version": version}
			pkgs_list.append(d)

	print(pkgs_list)
	
def add_arguments(parser):
	"""
	"""
	parser.add_argument(dest="install", nargs="*")


