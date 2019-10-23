#! /usr/bin/env python
import sys, os, getopt, pathlib, urllib.request, json, argparse
import list, show, install, uninstall, publish, deploy

# add common python scripts to the path
sys.path.append(os.fspath(pathlib.Path(__file__).parent.parent.joinpath('common')))

class Command(object):
	def __init__(self, name, help, required=True,  args_provider=None, runner=None):
		self.name = name
		self.help = help
		self.required = required
		self.args_provider = args_provider
		self.runner = runner

def main():
	commands = [
			Command('list', 'List all the packages', True, None, list.run),
	        Command('show', 'Show information about one or more installed packages', True, None, show.run),
	        Command('install', 'Install given package', True, install.add_arguments, install.run),
	        Command('uninstall', 'Uninstall given packages', True, uninstall.add_arguments, uninstall.run),
			Command('publish', 'Publish this package to repository', True, None, publish.run),
			Command('deploy', 'Deploy the application', True, deploy.add_arguments, deploy.run)
	       ]
	mainparser = argparse.ArgumentParser(description='Apama Package Manager Command Line Tool')
	cmd_parser = mainparser.add_subparsers(title='commands', dest='command')
	cmd_parser.required = True
	
	cmd_map = {} # runners map for dispatching the call
	for c in commands:
		argsp = cmd_parser.add_parser(c.name, help=c.help)
		if c.args_provider:
			c.args_provider(argsp)
		cmd_map[c.name] = c.runner

	args = mainparser.parse_args(sys.argv[1:])
	runner = cmd_map[args.command]
	runner(args)

if __name__=="__main__":
	main()
	