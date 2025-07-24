import sys, os, zlib
from .utils.utils import find_gitlite_repo, file_in_list
from ..commands.cat_file import read_file, parse_tree
from ..commands.index import read_index

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
		if file_in_list(index_paths, file) is False:
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


def no_options(files, path):
	index = read_index()
	if index is None:
		for file in files:
			print('error: pathspec \''f"{file}"'\' did not match any file(s) known to git')
	else:
		if validate_files(files, [entry['path'] for entry in index]) is False:
			sys.exit(1)
		for entry in index:
			content = read_file(entry['fields']['sha1']).body.decode()
			path = os.path.join(path.replace('.gitlite', ''), entry['path'])
			with open(path, 'w') as f:
				f.write(content)

def restore_changes(args, path):
	print(parse_tree(read_file(args.source).body))
	###I HAVE TO EXPAND THE DIRECTORIES!!! SAME FOR """NO OPTIONS""" FUNCTION

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
		print('ja')
		no_options(args.files, path)
	else:
		restore_changes(args, path)