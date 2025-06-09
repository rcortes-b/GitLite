import hashlib, os, zlib
from commands.utils import find_gitlite_repo

def hash_object(args):

	args.type = args.type if args.type else 'blob'
	try:
		with open(args.file, 'rb') as f:
			data = f.read()
		header = '{} {}'.format(args.type, len(data)).encode()
		full_data = header + b'\x00' + data
		sha1 = hashlib.sha1(full_data).hexdigest()
		if args.write:
			gitlite_path = find_gitlite_repo()
			if gitlite_path is not None:
				path = os.path.join(gitlite_path, 'objects', sha1[:2], sha1[2:])
				if not os.path.exists(path):
					os.makedirs(os.path.dirname(path), exist_ok=True)
					with open(path, 'wb') as fo:
						fo.write(zlib.compress(full_data))
		print(sha1)
	except FileNotFoundError:
		print('File couldn\'t be opened')
	