import os, sys
from commands.utils import find_gitlite_repo, get_all_files
from commands.index import *

def add(args):
	### Index file creation
	gitlite_path = find_gitlite_repo()
	index_path = os.path.join(gitlite_path, 'index')
	if not os.path.exists(index_path):
		f = open(index_path, 'w')
		f.close()
	### Check if every file is valid
	try:
		for files in args.files:
			if not os.path.exists(os.path.abspath(files)):
				raise Exception(files)
	except Exception as e:
		print(f"fatal: pathspec '{e}' did not match any files")
		sys.exit(1)
	### Get valid files, discard .gitliteignore paths
	all_files = get_all_files()
	arg_files = []
	if args.files:
		path = gitlite_path.replace('.gitlite', '')
		for files in args.files:
			normalized_path = os.path.abspath(files).replace(path, '')
			for f in all_files:
				if f == normalized_path:
					arg_files.append(f)
					print(f)
		#Check what to delete
		write_index(arg_files, index_path, 'ab')
	else:
		write_index(all_files, index_path, 'wb')
	print(read_index(index_path))
	#for f in all_files:
	#	print(f)
