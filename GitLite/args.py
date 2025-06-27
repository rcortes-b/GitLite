import argparse, sys
from commands.init import init
from commands.status import status
from commands.hash_object import hash_object
from commands.cat_file import cat_file
from commands.write_tree import write_tree
from commands.add import add
from commands.commit import commit

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
	hash_object_command.add_argument('-t', '--type', required=False, type=str, help='specify the type of the object to be created')
	hash_object_command.add_argument('file', help='File to be hashed and maybe stored')
	hash_object_command.set_defaults(func=hash_object)
	### CAT-FILE
	cat_file_command = commands.add_parser('cat-file', description='provide contents or details of repository objects')
	cat_file_group = cat_file_command.add_mutually_exclusive_group(required=False)
	cat_file_group.add_argument('-p', '--print', action='store_true', help='print the content of the object')
	cat_file_group.add_argument('-t', '--type', action='store_true', help='specify the type of the object')
	cat_file_group.add_argument('-s', '--size', action='store_true', help='the size of the object in bytes')
	cat_file_command.add_argument('object_type', help='type of the object', nargs='?')
	cat_file_command.add_argument('object', help='repository object which get information from')
	cat_file_command.set_defaults(func=cat_file)
	### WRITE-TREE
	write_tree_command = commands.add_parser('write-tree', description='creates a tree object from the current index')
	write_tree_command.add_argument('--prefix', required=False, type=str, help='specify the subdirectory which you will build the tree object')
	write_tree_command.set_defaults(func=write_tree)
	### ADD
	add_command = commands.add_parser('add')
	add_command.add_argument('files', nargs='*', help='files to be added to the index')
	add_command.add_argument('-A', '--all', action='store_true', help='add all the changes to the index')
	add_command.set_defaults(func=add)
	### COMMIT
	commit_command = commands.add_parser('commit')
	commit_command.add_argument('-m', '--message', required=True, help='define the commit message' )
	commit_command.set_defaults(func=commit)
	### STATUS
	status_command = commands.add_parser('status')
	status_command.set_defaults(func=status)
	return parser.parse_args()
