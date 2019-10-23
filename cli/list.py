import urllib.request, json


def run(args=None):
	"""
	list of packages
	"""
	print ("")
	print ("showing list of packages:")
	print ("")
	contents = urllib.request.urlopen("http://127.0.0.1:5000/packages")
	encoding = contents.info().get_content_charset('utf-8')
	manifests = json.loads(contents.read().decode(encoding))
	manifest_list = manifests["packages"]
	for elem in manifest_list:
		print(elem["name"] + "==" + elem["version"] if "version" in elem  else "")
		if "dependencies" in elem:
			for deps in elem["dependencies"]:
				print(deps["name"] + "==" + deps["version"] if "version" in deps  else "")
				
