import os
from commands.utils import find_gitlite_repo, get_all_files

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
	###
	all_files = get_all_files()
	for f in all_files:
		print(f)
