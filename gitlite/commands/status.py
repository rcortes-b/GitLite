import os, sys
from .utils.utils import get_ignored_files, get_all_files, find_gitlite_repo, file_in_list, status_default_msg
from .utils.objects import hash_blob, get_commit_files
from .index import read_index

# work tree not tracked by git and not in gitignore
# index and work tree
# index and commit

def message_check(message_trigger, mode=0):
	if message_trigger is False:
		if mode == 0:
			print('Changes to be committed:')
			print('  (use "git rm --cached <file>..." to unstage)')
		elif mode == 1:
			print('\nChanges not staged for commit:')
			print('  (use "git add <file>..." to update what will be committed)')
		else:
			print('\nUntracked files:')
			print('  (use "git add <file>..." to include in what will be committed)')
	return True

def changes_to_commit(entries=None, all_files=None, index_paths=None):
	message_trigger = False
	commit_files = get_commit_files()
	if entries is None and commit_files is None:
		print('No commits yet\n')
		message_trigger = True
	else:
		if commit_files is None:
			print('No commits yet\n')
			for entry in entries:
				for file in all_files:
					if entry['path'] == file:
						message_trigger = message_check(message_trigger)
						print('\t', f"\033[92m new file:\t{entry['path']}\033[0m")
		else:
			commit_paths = [commit['path'] for commit in commit_files]
			if entries is not None:
				for entry in entries:
					if file_in_list(commit_paths, entry['path']) is False:
						message_trigger = message_check(message_trigger)
						print('\t', f"\033[92m new file:\t{entry['path']}\033[0m")
					else:
						for files in commit_files:
							if file_in_list(index_paths, files['path']) is False:
								message_trigger = message_check(message_trigger)
								print('\t', f"\033[92m deleted:\t{files['path']}\033[0m")
							elif entry['path'] == files['path']:
								if entry['fields']['sha1'] != files['sha']:
									message_trigger = message_check(message_trigger)
									print('\t', f"\033[92m modified:\t{entry['path']}\033[0m")
								commit_files.remove(files)
			else:
				for files in commit_files:
					message_trigger = message_check(message_trigger)
					print('\t', f"\033[92m deleted:\t{files['path']}\033[0m")
	return message_trigger

def changes_to_add(entries=None, all_files=None, path=None):
	message_trigger = False
	if entries is None:
		return message_trigger
	elif all_files is None:
		message_trigger = message_check(message_trigger, mode=1)
		for entry in entries:
			print('\t', f"\033[91m deleted:\t{entry['path']}\033[0m")
	else:
		for entry in entries:
			if file_in_list(all_files, entry['path']) is True:
				if entry['fields']['sha1'] != hash_blob(os.path.join(path, entry['path']), False):
					message_trigger = message_check(message_trigger, mode=1)
					print('\t', f"\033[91m modified:\t{entry['path']}\033[0m")
			else:
				message_trigger = message_check(message_trigger, mode=1)
				print('\t', f"\033[91m deleted:\t{entry['path']}\033[0m")
	return message_trigger

def untracked_files(all_files=None, path_index_entries=None):
	message_trigger = False
	if path_index_entries is None:
		if all_files is None:
			return message_trigger
		for file in all_files:
			message_trigger = message_check(message_trigger, mode=2)
			print('\t', f"\033[91m{file}")
	else:
		if all_files:
			for file in all_files:
				if file_in_list(path_index_entries, file) is False:
					message_trigger = message_check(message_trigger, mode=2)
					print('\t', f"\033[91m{file}")
	return message_trigger

def status(args):
	path = find_gitlite_repo(False)
	if path is None:
		print('fatal: not gitlite repository found')
		sys.exit(1)
	index_entries = read_index()
	if index_entries is not None and len(index_entries) == 0:
		index_entries = None
	path_index_entries = None
	if index_entries is not None:
		path_index_entries = [entry['path'] for entry in index_entries]
	all_files = get_all_files()
	if all_files is None and index_entries is None:
		if get_commit_files() is None:
			status_default_msg()
			sys.exit(0)
	print('On branch master')
	trigger_commit = changes_to_commit(index_entries, all_files, path_index_entries)
	trigger_add = changes_to_add(index_entries, all_files, path)
	trigger_untracked = untracked_files(all_files, path_index_entries)
	if not (trigger_commit or trigger_add or trigger_untracked):
		print('nothing to commit, working tree clean')