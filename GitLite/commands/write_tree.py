from commands.utils.objects import hash_tree
from commands.utils.utils import find_gitlite_repo
import hashlib, os, zlib
def write_tree(path=find_gitlite_repo(False)):
	data, tree_data = hash_tree(path)
	path = os.path.join(path, '.gitlite', 'objects', data['sha1'][:2], data['sha1'][2:])
	if not os.path.exists(path):
		os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'wb') as fo:
		fo.write(zlib.compress(tree_data))
	print(data['sha1'])
