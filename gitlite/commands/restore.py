import sys, os, zlib
from .utils.utils import find_gitlite_repo, file_in_list, get_all_files
from .utils.objects import get_tree_files
from ..commands.cat_file import read_file, parse_tree
from ..commands.index import read_index, create_index_entry, write_index
from ..commands.add import expand_directory

def get_head_commit(path):
	path = os.path.join(path, 'refs/heads/main')
	if not os.path.exists(path):
		print('fatal: could not resolve HEAD')
		sys.exit(1)
	with open(path, 'r') as f:
		sha = f.read().replace('\n', '')
	commit_body = read_file(sha).body.decode()
	return commit_body[5:45]

def validate_files(files, index_paths):
	trigger = True
	for file in files:
		if os.path.isdir(file):
			expanded_files = expand_directory(file, [], get_all_files(), find_gitlite_repo(False) + '/')
			trigger = False
			for expanded in expanded_files:
				if file_in_list(index_paths, expanded) is True:
					trigger = True
			if trigger is False:
				print('error: pathspec \''f"{file}"'\' did not match any file(s) known to git')
		elif file_in_list(index_paths, file) is False:
			print('error: pathspec \''f"{file}"'\' did not match any file(s) known to git')
			trigger = False
	return trigger

def get_source_type(file, str):
	type = zlib.decompress(file.read())[:4].decode()
	if type == 'blob':
		print('fatal: reference is not a tree: 'f"{str}"'')
		sys.exit(1)
	if type == 'comm':
		commit_body = read_file(str).body.decode()
		str = commit_body[5:45]
	return str

def check_valid_source(str, path):
	if len(str) != 40:
		print('fatal: could not resolve 'f"{str}"'')
		sys.exit(1)
	path = os.path.join(path, 'objects', str[:2], str[2:])
	if not os.path.exists(path):
		print('fatal: could not resolve 'f"{str}"'')
		sys.exit(1)
	with open (path, 'rb') as f:
		str = get_source_type(f, str)
	return str


def restore_no_options(files, path):
	index = read_index()
	if index is None:
		for file in files:
			print('error: pathspec \''f"{file}"'\' did not match any file(s) known to git')
	else:
		if validate_files(files, [entry['path'] for entry in index]) is False:
			sys.exit(1)
		path = path.replace('.gitlite', '')
		all_files = get_all_files()
		for file in files:
			expand_dir = file
			if os.path.isdir(file):
				expand_dir = expand_directory(file, [], all_files, path)
			for expanded in expand_dir:
				for entry in index:
					if expanded == entry['path']:
						content = read_file(entry['fields']['sha1']).body.decode()
						new_path = os.path.join(path, entry['path'])
						with open(new_path, 'w') as f:
							f.write(content)

def restore_file(file, restore_index, restore_workdir, index, path, entries):
	content = read_file(file['sha']).body
	if restore_workdir is True or restore_index is False:
		new_content = content.decode()
		new_path = os.path.join(path, file['path'])
		with open(new_path, 'w') as f:
			f.write(new_content)
	elif restore_index is True:
		if index is not None:
			for entry in index:
				if file['path'] == entry['path']:
					index.remove(entry)
		entries.append(create_index_entry(file['path'], content))

	return index, entries
			
def restore_changes(args, path):
	index = read_index()
	entries = []
	source_files = get_tree_files(args.source)
	all_files = get_all_files()
	path = path.replace('.gitlite', '')
	for files in args.files:
		expand_dir = []
		expand_dir.append(files)
		if os.path.isdir(files):
			expand_dir = expand_directory(files, [], all_files, path)
			#print('files', files, expand_dir)
			#expand_dir.remove(files)
		for expanded in expand_dir:
			for source in source_files:
				if source['path'] == expanded:
					index, entries = restore_file(source, args.staged, args.worktree, index, path, entries)
	if args.staged:
		write_index(None, os.path.join(path, '.gitlite/index'), index, entries)

def restore(args):
	path = find_gitlite_repo()
	if path is None:
		print('fatal: not a gitlite repository (or any of the parent directories): .gitlite')
		sys.exit(1)
	if args.source:
		args.source = check_valid_source(args.source, path)
	elif args.staged is True:
		args.source = get_head_commit(path)
	if len(args.files) == 0:
		print('fatal: you must specify path(s) to restore')
		sys.exit(1)
	if not (args.source and args.staged):
		restore_no_options(args.files, path)
	else:
		restore_changes(args, path)