#! /usr/bin/env python
import sys, os, getopt, pathlib

# add common python scripts to the path
sys.path.append(os.fspath(pathlib.Path(__file__).parent.parent.joinpath('common')))

def printUsage():
	print ("apama_package_manager.py")
	print ("")
	print ("Options")
	print ("")
	print ("		--list			| list all the packages")

def list_packages():
	"""
	list of packages
	"""
	print ("showing list of packages:")

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