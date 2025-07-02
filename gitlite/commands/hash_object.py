from .utils.utils import find_gitlite_repo
from .utils.objects import hash_blob

def hash_object(args):

	args.type = args.type if args.type else 'blob'
	try:
		if args.type == 'blob':
			sha1 = hash_blob(args.file, args.write)
			print(sha1)
		elif args.type == 'tree':
			print('tree')
		else:
			print('commit')
	except FileNotFoundError:
		print('File couldn\'t be opened')
