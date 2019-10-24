import subprocess, os, shutil, sys

def run(args=None):
	"""
	"""
	deployDir = os.path.abspath(args.deployDir)
	if os.path.exists(deployDir): shutil.rmtree(deployDir)


	# Create a .dependencies file - required by engine_deploy
	try:
		with open('.dependencies', 'w') as fp:
			fp.write('<?xml version="1.0" encoding="UTF-8"?>\n<apama-project/>\n')
		subprocess.call(['engine_deploy' + ('.exe' if sys.platform in ['win32', 'cygwin'] else ''), '--exclude', '**/apama_packages.json', '-d', deployDir, '.'])
	finally:
		if os.path.exists('.dependencies'):
			os.remove('.dependencies')

def add_arguments(parser):
	"""
	"""
	parser.add_argument(dest="deployDir")