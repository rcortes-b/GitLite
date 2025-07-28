import hashlib, os, zlib, sys
from .utils import find_gitlite_repo, get_ignored_files, dir_in_list, get_all_files
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

def hash_tree(path=None, entries=None, dirname='', dir=''):
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
		if entries is not None:
			for entry in entries:
				if entry['path'] == files:
					body.append({'mode': entry['fields']['mode'],
								'type': 'blob',
								'path': files.replace(dirname + '/', ''),
								'sha1': entry['fields']['sha1']})
	ignored_dirs = get_ignored_files()
	for dirs in sorted(walk_tuple[0][1]):
		if dir_in_list(ignored_dirs, dirs) is False:
				body_tree, _ = hash_tree(os.path.join(path, dirs), entries, os.path.join(dirname, dirs), dirs) # os.path.join(dirname, dirs)
				#print(dirs)
				if body_tree is not None:
					#print(dirs)
					body.append(body_tree)
	if len(body) == 0 and dirname != '':
		return None, None
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
			 'path': dir,
			 'sha1': sha1}, tree_object)

def get_commit_files():
	path = os.path.join(find_gitlite_repo(), 'refs/heads/main')
	if not os.path.exists(path):
		return None

	with open(path, 'r') as f:
		sha = f.read().replace('\n', '')
	commit_body = read_file(sha).body.decode()
	tree_sha = commit_body[5:45]
#	parent_tree = parse_tree(read_file(tree_sha).body)
#
#	for files in parent_tree:
#		if files['obj_type'] == 'tree':
#			sub_tree = parse_tree(read_file(files['sha']).body)
#			parent_tree.remove(files)
#			for sub_files in sub_tree:
#				parent_tree.append(sub_files)
#	return parent_tree
	return get_tree_files(tree_sha)

def get_tree_files(tree_sha):
	parent_tree = parse_tree(read_file(tree_sha).body)

	for files in parent_tree:
		if files['obj_type'] == 'tree':
			sub_tree = parse_tree(read_file(files['sha']).body)
			parent_tree.remove(files)
			for sub_files in sub_tree:
				sub_files['path'] = os.path.join(files['path'], sub_files['path'])
				parent_tree.append(sub_files)
	return parent_tree