import os, shutil, json

def run(args=None):
	"""
	"""
	projectPath = os.path.abspath(args.projectName)
	if os.path.exists(projectPath):
		raise Exception(f'Can\'t create {projectPath}, directory with the same name already exists')

	os.makedirs(projectPath, exist_ok=True)

	projectTemplate = {
		'name': os.path.basename(projectPath),
		'description': '',
		'version': '1.0.0',
		'tags': [],
		'dependencies': [],
	}

	with open(os.path.join(projectPath, 'apama_packages.json'), 'w') as fp:
		json.dump(projectTemplate, fp, indent=2)

def add_arguments(parser):
	"""
	"""
	parser.add_argument(dest="projectName")
