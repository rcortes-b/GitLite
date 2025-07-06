import os, sys
from .utils.utils import get_ignored_files, get_all_files, find_gitlite_repo, file_in_list, status_default_msg
from .utils.objects import hash_blob, get_commit_files
from .index import read_index

# work tree not tracked by git and not in gitignore
# index and work tree
# index and commit

def status(args):
	path = find_gitlite_repo(False)
	if path is None:
		print('fatal: not gitlite repository found')
		sys.exit(1)
	index_entries = read_index()
	path_index_entries = None
	if index_entries is not None:
		path_index_entries = [entry['path'] for entry in index_entries]
	ignored_files = get_ignored_files()
	all_files = get_all_files()
	if all_files is None and index_entries is None:
		status_default_msg()
		sys.exit(0)
	if index_entries is not None:
		print('On branch master')
		print('Your branch is up to date with \'origin/main\'.\n')
		print('Changes to be committed:')
		#index and commit
		commit_files = get_commit_files()
		if commit_files is not None:
			for index in index_entries:
				found = False
				for commit in commit_files:
					if index['path'] == commit['path']:
						if index['fields']['sha1'] != commit['sha']:
							print('\t', f"\033[92m modified:\t{index['path']}\033[0m")
						commit_files.remove(commit)
						found = True
						break
				if found is False:
					print('\t', f"\033[92m new file:\t{index['path']}\033[0m")
			if len(commit_files) > 0:
				for removed_file in commit_files:
					print('\t', f"\033[91m removed:\t{removed_file['path']}\033[0m")
		print('\nChanges not staged for commit:')
		#index and work tree
		for entry in index_entries:
			if file_in_list(all_files, entry['path']) is True:
				if entry['fields']['sha1'] != hash_blob(os.path.join(path, entry['path']), False):
					print('\t', f"\033[91m modified:\t{entry['path']}\033[0m")
			else:
				print('\t', f"\033[91m deleted:\t{entry['path']}\033[0m")
	else:
		print('On branch master\n\nNo commits yet')
	if all_files is not None:
		print('\nUntracked files:')
		#print(index_entries)
		for file in all_files:
			if file_in_list(path_index_entries, file) is False:
				print('\t', f"\033[91m{file}")
		
			
	#print('\n\n', all_files)
	#work tree and not tracked by git and not gitignore
