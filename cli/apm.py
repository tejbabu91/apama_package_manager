#! /usr/bin/env python
import sys, os, getopt, pathlib, urllib.request, json

# add common python scripts to the path
sys.path.append(os.fspath(pathlib.Path(__file__).parent.parent.joinpath('common')))

def printUsage():
	print ("These are the common command used in various situations")
	print ("")
	print ("		--list				|	List all the packages")
	print ("		--install			|	Install given package")
	print ("		--uninstall			|	Uninstall given packages")
	print ("		--show				|	Show information about one or more installed packages")
	print ("		--deploy			|	Deploy the application")
	print ("		--publish			|	Publish this package to repository")

def list_packages():
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

def install(package):
	"""
	packages can be a string or list of strings
	"""
	print("installs the mentioned packages.")

def uninstall(package):
	"""
	packages can be a string or list of strings
	"""
	print("uninstall the mentioned packages.")

def show(package):
	"""
	packages can be a string or list of strings
	"""
	print("show information of one or more mentioned packages.")
	
def deploy():
	"""
	deploy
	"""
	print("deploy")

def publish():
	"""
	publish
	"""
	print("publish")	

def main(args):
	optionString = "hli:u:s:dp"
	optionList = ["help", "list", "install=", "uninstall=", "show=", "deploy", "publish"]
	
	try:
		optionlist, arguments = getopt.getopt(args, optionString, optionList)
		if arguments: raise Exception(str(arguments))
	except:
		print ("Error parsing command line arguments: %s" % (sys.exc_info()[1]))
		return 1
	
	for option, value in optionlist:
			if option in ["-h", "--help"]:
				printUsage()
				return 0
			elif option in ["-l", "--list"]:
				list_packages()
				return 0
			elif option in ["-i", "--install"]:
				install(value)
				return 0
			elif option in ["-u", "--uninstall"]:
				uninstall(value)
				return 0
			
			elif option in ["-s", "--show"]:
				show(value)
				return 0
			elif option in ["-d", "--deploy"]:
				deploy(value)
				return 0
			elif option in ["-d", "--publish"]:
				publish(value)
				return 0

if __name__=="__main__":
	sys.exit(main(sys.argv[1:]))