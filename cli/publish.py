import os
import zipfile
import hashlib
from helper import upload_package

def get_all_files():
	ret = list()
	baseDir = './'
	for f in os.listdir(baseDir):
		if os.path.isdir(f):
			if os.path.basename(f) == 'apama_packages':
				continue
			# get recursive list of files
			for root, dirs, files in os.walk(f):
				ret.extend([baseDir + root + '/' + ff for ff in files])
			continue
		if f not in ['package.zip', 'checksums.txt']:
			ret.append(baseDir + f)
	return ret

def generate_md5_hash_for_all_files(file_paths):
	with open('checksums.txt', 'w') as fp:
		for f in file_paths:
			with open(f, "rb") as inp:
				fp.write(f'{hashlib.md5(inp.read()).hexdigest()} {f}\n')
	file_paths.append('./checksums.txt')

def run(args=None):
	"""
	"""
	name = 'package.zip'
	all_files = get_all_files()
	generate_md5_hash_for_all_files(all_files)

	with zipfile.ZipFile(name, 'w') as zip:
		for f in all_files:
			zip.write(f)

	upload_package(name)

	os.remove('checksums.txt')
	os.remove(name)

if __name__ == "__main__":
	#get_all_files()
	print(get_all_files())