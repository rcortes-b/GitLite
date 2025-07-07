from .utils.objects import hash_blob

def hash_object(args):
	try:
			sha1 = hash_blob(args.file, args.write)
			print(sha1)
	except FileNotFoundError:
		print('fatal: file couldn\'t be opened')
