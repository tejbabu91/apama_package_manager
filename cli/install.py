import urllib.request

def run(args=None):
	"""
	"""
	pkgs_list = []
	pkgs = vars(args)
	for item in pkgs["install"]:
		name=None
		version=None
		if ":" in item:
			name, version = item.split(":")
		else:
			name = item
		d = {"name":name, "version": version}
		pkgs_list.append(d)
	print(pkgs_list)
	
def add_arguments(parser):
	"""
	"""
	parser.add_argument(dest="install", nargs="+")
	