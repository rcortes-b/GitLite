import os, sys
from .utils.utils import find_gitlite_repo, get_all_files
from .index import *

def add(args):
	### Index file creation
	if not args.files and args.all is False:
		print("error: no files specified for 'add'")
		print("usage: gitlite add <file> [...] or gitlite add --all/-A")
		sys.exit(1)
	gitlite_path = find_gitlite_repo()
	if gitlite_path is None:
		print('fatal: not gitlite repository found')
		sys.exit(1)
	index_path = os.path.join(gitlite_path, 'index')
	if not os.path.exists(index_path):
		f = open(index_path, 'w')
		f.close()

	### Get valid files, discard .gitliteignore paths
	all_files = get_all_files()
	arg_files = []

	if args.files:
		path = gitlite_path.replace('.gitlite', '')
		index_entries = read_index()

		for files in args.files:
			normalized_path = os.path.abspath(files).replace(path, '')
			for f in all_files:
				if f == normalized_path and index_entries is not None:
					for entry in index_entries:
						if entry['path'] == f:
							print('f', f)
							index_entries.remove(entry)
				elif f == normalized_path and index_entries is None:
					arg_files.append(f)
		if arg_files:
			all_files = arg_files
		write_index(all_files, index_path, index_entries)
	else:
		write_index(all_files, index_path)

