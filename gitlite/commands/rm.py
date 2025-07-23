import os, sys
from .utils.utils import find_gitlite_repo, file_in_list, get_all_files
from ..commands.index import read_index, write_index
from ..commands.add import expand_directory
from .utils.objects import get_commit_files

class fileData:
	def __init__(self, name, type, to_delete, args):
		self.name = name
		self.type = type
		self.delete = to_delete
		if self.type == 1 and args.r is False:
			print('fatal: not removing \'c\' recursively without -r')
			sys.exit(1)
		

def parse_data(args, path):
	data = []
	for files in args.files:
		if os.path.isdir(files):
			if args.r is False:
				print('fatal: not removing \'c\' recursively without -r')
				sys.exit(1)
			args.files = expand_directory(files, args.files, get_all_files(), path  + '/')
			data.append(fileData(files, True, args))
			continue
		normalized_path = os.path.abspath(files).replace(path + '/', '')
		data.append(fileData(normalized_path, os.path.isdir(normalized_path), args))
	return data

def checker(args, data, index):
	if index is None:
		print('fatal: pathspec \''f"{args.files[0]}"'\' did not match any files')
		sys.exit(1)
	else:
		index_entries = [entry['path'] for entry in index]
		for files in args.files:
			if file_in_list(index_entries, files) is False and os.path.isdir(files) is False:
				print('fatal: pathspec \''f"{files}"'\' did not match any files')
				sys.exit(1)
	if args.force is False and args.cached is False:
		trigger = False
		commit_files = get_commit_files()
		if commit_files is None:
			print('error: the following files have changes staged in the index:')
			for obj in data:
				print('\t'f"{obj.name}"'')
			print('(use --cached to keep the file, or -f to force removal)')
			sys.exit(1)
		for obj in data:
			for entry in index:
				if entry['path'] == obj.name:
					for commit in commit_files:
						if commit['path'] == entry['path']:
							if commit['sha'] != entry['fields']['sha1']:
								if trigger is False:
									print('error: the following files have changes staged in the index:')
									trigger = True
								print('\t'f"{obj.name}"'')
		if trigger is True:
			print('(use --cached to keep the file, or -f to force removal)')
			sys.exit(1)

def delete_files(data, index, is_cached):
	dirs = []
	for obj in data:
		if obj.type == 1:
			dirs.append(obj)
			continue
		for entry in index:
			if obj.name == entry['path']:
				index.remove(entry)
				if is_cached is False:
					os.remove(os.path.abspath(obj.name))
				print('rm \''f"{obj.name}"'\'')
				break
	for dir in dirs:
		### CHECK DIRECTORY SIZE, IF ITS 0, remove
			os.rmdir(os.path.abspath(dir.name))
	path = os.path.join(find_gitlite_repo(), 'index')
	if len(index) == 0:
		index = None
	write_index(None, path, index)

def rm(args):
	if len(args.files) == 0:
		print('fatal: No pathspec was given. Which files should I remove?')
		sys.exit(1)
	index = read_index()
	path = find_gitlite_repo(False)
	data = parse_data(args, path)
	checker(args, data, index)
	delete_files(data, index, args.cached)
	### COMPROBAR QUE PASA CUANDO UN FILE ES DIRECTORY Y QUE ERROR SALE EN CASO DE QUERER HACERLO CON LA -r OPTION
	#-r --force --cached