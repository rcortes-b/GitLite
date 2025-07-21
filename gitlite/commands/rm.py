import os, sys
from .utils.utils import find_gitlite_repo, file_in_list
from ..commands.index import read_index
from .utils.objects import get_commit_files

class fileData:
	def __init__(self, name, type, args):
		self.name = name
		self.type = type
		self.cached = args.cached
		self.r = args.r
		if self.type == 1 and self.r is False:
			print('fatal: not removing \'c\' recursively without -r')
			sys.exit(1)
		

def parse_data(args, path):
	data = []
	for files in args.files:
		normalized_path = os.path.abspath(files).replace(path + '/', '')
		data.append(fileData(normalized_path, os.path.isdir(normalized_path), args))
		print('normalized_path: ', normalized_path)
		if os.path.isdir(normalized_path):
			print(os.path.isdir(normalized_path))
		else:
			print('is not dir')
	return data

def checker(args, data, index):
	if index is None:
		print('fatal: pathspec \''f"{args.files[0]}"'\' did not match any files')
		sys.exit(1)
	else:
		index_entries = [entry['path'] for entry in index]
		for files in args.files:
			if file_in_list(index_entries, files) is False:
				print('fatal: pathspec \''f"{files}"'\' did not match any files')
				sys.exit(1)
	if args.force is False and args.cached is False:
		trigger = False
		commit_files = get_commit_files()
		if commit_files is None:
			print('error: the following files have changes staged in the index:')
			for files in args.files:
				print('\t'f"{files}"'')
			print('(use --cached to keep the file, or -f to force removal)')
			sys.exit(1)
		print('commit_files',commit_files)
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

### File == type 0
### dir  == type 1

def rm(args):
	if len(args.files) == 0:
		print('fatal: No pathspec was given. Which files should I remove?')
		sys.exit(1)
	index = read_index()
	path = find_gitlite_repo(False)
	data = parse_data(args, path)
	checker(args, data, index)
	

	#-r --force --cached