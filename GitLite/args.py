import argparse, sys
from commands.init import init
from commands.status import status
from commands.hash_object import hash_object

def load_arguments(parser):
	parser.add_argument('-v', '--version', action='version', version='GitLite Version 0.0.1', help='check the current gitlite version')
	#add another flag as argument

def parse_args():
	parser = argparse.ArgumentParser(prog='GitLite', description="A minimal git implementation", epilog="Thanks for using the program!")	
	load_arguments(parser)

	commands = parser.add_subparsers(dest="commands", required=True)
	### INIT
	init_command = commands.add_parser('init')
	init_command.add_argument('repo_name', nargs='?', type=str, help='Name of the repository to be created')
	init_command.set_defaults(func=init)
	### HASH-OBJECT
	hash_object_command = commands.add_parser('hash-object')
	hash_object_command.add_argument('-w', '--write', required=False, action='store_true', help='store the object hashed')
	hash_object_command.add_argument('-t', '--type', required=False, type=str, help='specify the type of object to be created')
	hash_object_command.add_argument('file', help='File to be hashed and maybe stored')
	hash_object_command.set_defaults(func=hash_object)
	### STATUS
	status_command = commands.add_parser('status')
	status_command.set_defaults(func=status)
	return parser.parse_args()
