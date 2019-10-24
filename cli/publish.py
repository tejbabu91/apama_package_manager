import os
import zipfile
import http.client
import hashlib

def generate_md5_hash_for_all_files(file_paths):
	file_to_md5 = dict()
	for file in file_paths:
		with open(file, "rb") as f:
			file_to_md5[file] = hashlib.md5(f.read()).hexdigest()
	with open('files_md5.txt', 'w') as f:
		for k, v in file_to_md5.items():
			path = os.path.abspath(k)
			f.write(v+' '+path+'\n')

	file_paths.append('files_md5.txt')

def get_all_file_paths(path):
	file_paths = []
	for root, dirs, files in os.walk(path):
		if 'apama_packages' in dirs:
			dirs.remove('apama_packages')
		for file in files:
			filepath = os.path.join(root, file)
			file_paths.append(filepath)
	return file_paths

def run(args=None):
	"""
	"""
	name = args.package_name
	file_paths = get_all_file_paths('./')
	generate_md5_hash_for_all_files(file_paths)

	with zipfile.ZipFile(name+'.zip', 'w') as zip:
		for file in file_paths:
			zip.write(file)

	content = open(name+".zip", 'rb').read()
	
	headers = {"Content-type": "application/octet-stream"}

	conn = http.client.HTTPConnection('jupiter.apama.com', port=5000)
	conn.request("POST", "/packages", content, headers)
	resp = conn.getresponse()
	if resp.status == 200:
		print('package published successfully')

def add_arguments(parser):
	"""
	"""
	parser.add_argument(dest="package_name")
