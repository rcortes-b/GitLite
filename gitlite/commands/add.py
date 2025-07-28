import os, sys
from .utils.utils import find_gitlite_repo, get_all_files, file_in_list
from .index import *

def expand_directory(dir, list_object, all_files, path):
	rm_expansor = False
	if len(list_object) == 0:
		rm_expansor = True
	for rootdir, dirname, filenames in os.walk(os.path.abspath(dir)):
		if rm_expansor is True:
			for dirs in dirname:
				list_object.append(os.path.join(rootdir,dirs).replace(path, ''))
		for files in filenames:
			file = os.path.join(rootdir, files).replace(path, '')
			if file_in_list(all_files, file) is True: ### Check if file is not ignored
				list_object.append(file)
	return list_object
		

def empty_repository(files, entries, path):
	if files:
		for file in files:
			for entry in entries:
				if file == entry['path']:
					entries.remove(entry)
					break
	else:
		entries.clear()
	if len(entries) == 0:
		entries = None
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

	all_files = get_all_files()
	index_entries = read_index()

	if all_files is None and index_entries is None:
		return
	elif all_files is None:
		entries = empty_repository(args.files, index_entries, index_path)
		write_index(all_files, index_path, entries)
	else:
		arg_files = []
		if args.files:
			path = gitlite_path.replace('.gitlite', '')
			check_if_files_exists(args.files, index_entries, all_files)
			for files in args.files:
				if os.path.isdir(files):
					args.files = expand_directory(files, args.files, all_files, path)
					continue
				normalized_path = os.path.abspath(files).replace(path, '')
				if file_in_list(all_files, files) is True:
					for f in all_files:
						if f == normalized_path and index_entries is not None:
							for entry in index_entries:
								if entry['path'] == f:
									index_entries.remove(entry) ### Remove the old entry data of each args.files
						elif f == normalized_path and index_entries is None: ### If index doesnt exist, only the args.files will be added
							arg_files.append(f)
			if not arg_files:
				arg_files = [entry['path'] for entry in index_entries] ### Get every entry['path']
				for f in args.files:
					if not os.path.isdir(f):
						if file_in_list(all_files, f) is True:
							arg_files.append(f)
						else:
							arg_files.remove(f)
			all_files = arg_files
			write_index(all_files, index_path, index_entries)
		else:
			write_index(all_files, index_path, [])