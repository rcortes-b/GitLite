import os, sys
from .utils.utils import find_gitlite_repo, get_all_files
from .index import *

def empty_repository(files, entries, path):
	if entries is None:
		return None
	if files:
		for file in files:
			for entry in entries:
				if file == entry['path']:
					entries.remove(entry)
					break
	else:
		entries.clear()
	if len(entries) == 0:
		os.remove(path)
		f = open(path, 'w')
		f.close()
	return entries

def check_if_files_exists(files, entries, all_files):
	for file in files:
		found = False
		if os.path.exists(file):
			found = True
		else:
			for entry in entries:
				if entry['path'] == file:
					found = True
					break
			if found is False:
				for f in all_files:
					if f == file:
						found = True
						break
			if found is False:
				print(f"fatal: pathspec '{file}' did not match any files")
				sys.exit(1)

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
	if all_files is None and read_index() is None:
		return
	elif all_files is None:
		empty_repository(args.files, read_index(), index_path)
	else:
		arg_files = []
		if args.files:
			path = gitlite_path.replace('.gitlite', '')
			index_entries = read_index()
			check_if_files_exists(args.files, index_entries, all_files)
			for files in args.files:
				normalized_path = os.path.abspath(files).replace(path, '')
				for f in all_files:
					if f == normalized_path and index_entries is not None:
						for entry in index_entries:
							if entry['path'] == f:
								index_entries.remove(entry)
					elif f == normalized_path and index_entries is None:
						arg_files.append(f)
			if not arg_files:
				arg_files = [entry['path'] for entry in index_entries]
				for f in args.files:
					arg_files.append(f)
			all_files = arg_files
			write_index(all_files, index_path, index_entries)
		else:
			write_index(all_files, index_path)