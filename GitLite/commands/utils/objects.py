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

def hash_tree(abs_path=find_gitlite_repo(root=False)):
	body = []
	entries = read_index()
	for entry in entries:
		print(entry['path'])
	print('\n\n\n------------------\n\n\n')
	for rootdir, dirname, filenames in os.walk(abs_path):
		dir_name = rootdir.replace(abs_path + '/', '')
		dir_name = '' if dir_name == abs_path else dir_name
		if dir_name.find('.gitlite') > -1:
			continue
		print('dirname: ', dir_name)
		#print('rootdir', rootdir)
		for filename in filenames:
			for entry in entries:
				#print(entry['path'], os.path.join(dir_name, filename))
				if os.path.join(dir_name, filename)  == entry['path']:
					print('filename: ', entry['path'])

		
			