from _elementtree import SubElement
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment
import json, os

def run(args=None):
	"""
	"""
	pass
		
def prettify(elem):
	"""Return a pretty-printed XML string for the Element.
	"""
	rough_string = ElementTree.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")

def createDeploy(fileList):
	top = Element('configuration')
	intAttribute = SubElement(top, 'intAttribute')
	intAttribute.set('key', 'com.apama.text.CONFIG_VERSION')
	intAttribute.set('value', '3')
	listAttribute = SubElement(top, 'listAttribute')
	listAttribute.set('key', 'com.apama.text.COMPONENTS')
	listEntry = SubElement(listAttribute, 'listEntry')
	component = SubElement(listEntry, 'component')
	component.set('port', '15903')
	component.set('type', 'CORRELATOR')

	for runtimeEntry in fileList:
		runtimeDependencyEntry = SubElement(component, 'runtimeDependencyEntry')
		runtimeDependencyEntry.set('enabled', 'true')
		runtimeDependencyEntry.set('path', runtimeEntry)
		runtimeDependencyEntry.set('type', 'PROJECT_BUNDLE_MON_FILE')

	return prettify(top)

def createFileList(packageList):
	fileList = []
	for package in packageList:
		with open('package') as json_file:
			packageDate = json.load(json_file)
			# assumning that the package json file has a list of monitor files.
			fileList.append(packageList['monitors'])
	return fileList

def packageList():
	path = 'C:\\dev\\GitHub\\apama_package_manager\\examples'
	packageList = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(path):
		for file in f:
			if 'apama_packages.json' in file:
				packageList.append(os.path.join(r, file))
	return packageList

def add_arguments(parser):
	"""
	"""
	pass