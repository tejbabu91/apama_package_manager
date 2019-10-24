import os
import zipfile
import urllib.request
import http.client

def zipdir(path, ziph):
	for root, dirs, files in os.walk(path):
		for file in files:
			ziph.write(os.path.join(root, file))
			
def run(args=None):
	"""
	"""
	name = vars(args)["package"]
	zipf = zipfile.ZipFile(name+".zip", 'w', zipfile.ZIP_DEFLATED)
	zipdir('./', zipf)
	zipf.close()
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
	parser.add_argument(dest="package")
