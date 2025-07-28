import argparse
from .commands.init import init
from .commands.status import status
from .commands.hash_object import hash_object
from .commands.cat_file import cat_file
from .commands.write_tree import write_tree
from .commands.add import add
from .commands.commit import commit
from .commands.ls_files import ls_files
from .commands.rm import rm
from .commands.restore import restore

def load_arguments(parser):
	parser.add_argument('-v', '--version', action='version', version='GitLite Version 0.0.1', help='check the current gitlite version')
	#add another flag as argument

def parse_args():
	parser = argparse.ArgumentParser(prog='GitLite', description="A minimal git implementation", epilog="Thanks for using the program!")	
	load_arguments(parser)

	commands = parser.add_subparsers(dest="commands", required=True)
	### INIT
	init_command = commands.add_parser('init')
	init_command.add_argument('repo_name', nargs='?', type=str, help='name of the repository to be created')
	init_command.add_argument('--author', type=str, help='name of the repository owner')
	init_command.add_argument('--email', type=str, help='email adress of the repository owner')
	init_command.set_defaults(func=init)
	### HASH-OBJECT
	hash_object_command = commands.add_parser('hash-object')
	hash_object_command.add_argument('-w', '--write', required=False, action='store_true', help='store the object hashed')
	hash_object_command.add_argument('file', help='file to be hashed and maybe stored')
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
	### LS-FILES
	ls_files_command = commands.add_parser('ls-files', help='show all tracked files in gitlite index')
	ls_files_group = ls_files_command.add_mutually_exclusive_group(required=False)
	ls_files_group.add_argument('-c', '--cached', action='store_true', help='show all files cached in gitlite index, i.e. all tracked files')
	ls_files_group.add_argument('-s', '--stage', action='store_true', help='show staged contents; mode bits, object name and stage number in the output.')
	ls_files_group.add_argument('-d', '--deleted', action='store_true', help='show files with an unstaged deletion')
	ls_files_group.add_argument('-m', '--modified', action='store_true', help='show files with an unstaged modification')
	ls_files_group.add_argument('-o', '--others', action='store_true', help='show other (i.e. untracked) files in the output')
	ls_files_command.set_defaults(func=ls_files)
	### RM
	rm_command = commands.add_parser('rm', help='remove files matching pathspec from the index, or from the working tree and the index')
	rm_command.add_argument('files', nargs='*', help='files to remove or leading directory name')
	rm_command.add_argument('-f', '--force', action='store_true', help='override the up-to-date check.')
	rm_command.add_argument('--cached', action='store_true', help='use this option to unstage and remove paths only from the index')
	rm_command.add_argument('-r', action='store_true', help='allow recursive removal when a leading directory name is given')
	rm_command.set_defaults(func=rm)
	### RESTORE
	restore_command = commands.add_parser('restore', help='helps to unstage or even discard uncommitted local changes.')
	restore_command.add_argument('files', nargs='*', help='the name of a file (or multiple files) you want to restore')
	restore_command.add_argument('-s', '--source', type=str, help='specify the commitcto restore from')
	restore_command.add_argument('-S', '--staged', action='store_true', help='removes the file from the Staging Area, but leaves its actual modifications untouched')
	restore_command.add_argument('-W', '--worktree', action='store_true', help='restores the content from the working directory')
	restore_command.set_defaults(func=restore)
	return parser.parse_args()
