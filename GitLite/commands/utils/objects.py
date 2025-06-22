import hashlib, os, zlib
from commands.utils.utils import find_gitlite_repo
from commands.index import read_index

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
	return sha1

def hash_tree(path=find_gitlite_repo(root=False), entries=None, dirname=None):
	body = []
	if entries is None:
		entries = read_index()
	for entry in entries:
		print(entry['path'])
	#print('PATH: ', path)
	print('\n\n\n------------------\n\n\n')
	walk_tuple = list(os.walk(path))
	for files in sorted(walk_tuple[0][2]):
		for entry in entries:
			if entry['path'] == files:
				body.append({'mode': entry['fields']['mode'],
				 			 'type': 'blob',
				 			 'path': entry['path'],
							 'sha1': entry['fields']['sha1']})
	for dirs in sorted(walk_tuple[0][1]):
		body_tree, bs = hash_tree(os.path.join(path, dirs), entries, dirs)
		if body_tree is not None:
			body.append(body_tree)
	if body is None:
		return None
	body.sort(key=lambda x: x['path'])
	tree_data = b""
	for object in body:
		tree_data += f"{object['mode']} {object['path']}".encode() + b'\x00' + bytes.fromhex(object['sha1'])
	#for tree_files in sorted(body.):
	#	print('Tree files: ', tree_files)
	header = f"tree {len(tree_data)}\0".encode()
	tree_object = header + tree_data
	return ({'mode': '040000',
		  	 'type': 'tree',
			 'path': dirname,
			 'sha1': hashlib.sha1(tree_object).hexdigest()}, hashlib.sha1(tree_object).hexdigest())

		
			