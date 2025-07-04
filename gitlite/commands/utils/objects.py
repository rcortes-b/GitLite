import hashlib, os, zlib, sys
from .utils import find_gitlite_repo, get_ignored_files, dir_in_list
from ..index import read_index
from ..cat_file import read_file, parse_tree

def hash_blob(path, write):
	with open(path, 'rb') as f:
		data = f.read()
	header = '{} {}'.format('blob', len(data)).encode()
	full_data = header + b'\x00' + data
	sha1 = hashlib.sha1(full_data).hexdigest()
	if write:
		gitlite_path = find_gitlite_repo()
		if gitlite_path is not None:
			path = os.path.join(gitlite_path, 'objects', sha1[:2], sha1[2:])
			if not os.path.exists(path):
				os.makedirs(os.path.dirname(path), exist_ok=True)
				with open(path, 'wb') as fo:
					fo.write(zlib.compress(full_data))
		else:
			print('fatal: not gitlite repository found')
			sys.exit(1)
	return sha1

def hash_tree(path=None, entries=None, dirname=''):
	if path is None:
		path = find_gitlite_repo(root=False)
		if path is None:
			print('fatal: not gitlite repository found')
			sys.exit(1)
	body = []
	if entries is None:
		entries = read_index()

	walk_tuple = list(os.walk(path))
	for files in sorted(walk_tuple[0][2]):
		files = os.path.join(dirname, files)
		for entry in entries:
			if entry['path'] == files:
				body.append({'mode': entry['fields']['mode'],
				 			 'type': 'blob',
				 			 'path': entry['path'],
							 'sha1': entry['fields']['sha1']})
	ignored_dirs = get_ignored_files()
	for dirs in sorted(walk_tuple[0][1]):
		if dir_in_list(ignored_dirs, dirs) is False:
				body_tree, _ = hash_tree(os.path.join(path, dirs), entries, os.path.join(dirname, dirs)) # os.path.join(dirname, dirs)
				if body_tree is not None:
					body.append(body_tree)
	if body is None:
		return None
	body.sort(key=lambda x: x['path'])
	tree_data = b""
	for object in body:
		tree_data += f"{object['mode']} {object['path']}".encode() + b'\x00' + bytes.fromhex(object['sha1'])
	header = f"tree {len(tree_data)}\0".encode()
	tree_object = header + tree_data
	sha1 = hashlib.sha1(tree_object).hexdigest()
	path = os.path.join(find_gitlite_repo(False), '.gitlite', 'objects', sha1[:2], sha1[2:])
	if not os.path.exists(path):
		os.makedirs(os.path.dirname(path), exist_ok=True)
		with open(path, 'wb') as fo:
			fo.write(zlib.compress(tree_object))
	return ({'mode': '040000',
		  	 'type': 'tree',
			 'path': dirname,
			 'sha1': sha1}, tree_object)

def get_commit_files():
	print('GET COMMIT FILES START')
	path = find_gitlite_repo()
	with open(os.path.join(path, 'refs/heads/main'), 'r') as f:
		sha = f.read().replace('\n', '')
	commit_body = read_file(sha).body.decode()
	tree_sha = commit_body[5:45]
	print(tree_sha)
	parent_tree = parse_tree(read_file(tree_sha).body)
	print(parent_tree)
	print('GET COMMIT FILES END')