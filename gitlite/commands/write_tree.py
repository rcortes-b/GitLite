import os, zlib, sys
from .utils.objects import hash_tree
from .utils.utils import find_gitlite_repo
def write_tree(args=None):
	path=None
	try:
		if args and args.prefix:
			if not os.path.exists(os.path.join(os.path.abspath('.'), args.prefix)):
				raise Exception('subdirectory is not valid')
			path = os.path.join(os.path.abspath('.'), args.prefix)
		else:
			path = find_gitlite_repo(False)
			if path is None:
				print('fatal: not gitlite repository found')
				sys.exit(1)
		data, tree_data = hash_tree()
		path = find_gitlite_repo(False)
		if path is None:
			print('fatal: not gitlite repository found')
			sys.exit(1)
		path = os.path.join(path, '.gitlite', 'objects', data['sha1'][:2], data['sha1'][2:])
		if not os.path.exists(path):
			#print(os.path.dirname(path))
			os.makedirs(os.path.dirname(path), exist_ok=True)
		with open(path, 'wb') as fo:
			fo.write(zlib.compress(tree_data))
		print(data['sha1'])
	except Exception as e:
		print(f'fatal: {e}') 
