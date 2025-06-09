import argparse, sys
from commands.init import init
from commands.status import status

def load_arguments(parser):
	parser.add_argument('-v', '--version', action='version', version='GitLite Version 0.0.1', help='check the current gitlite version')
	#add another flag as argument

def parse_args():
	parser = argparse.ArgumentParser(prog='GitLite', description="A minimal git implementation", epilog="Thanks for using the program!")	
	load_arguments(parser)

	commands = parser.add_subparsers(dest="commands", required=True)
	init_command = commands.add_parser('init')
	init_command.add_argument('repo_name', type=str, help='Name of the repository to be created')
	init_command.set_defaults(func=init)
	status_command = commands.add_parser('status')
	status_command.set_defaults(func=status)
	return parser.parse_args()
