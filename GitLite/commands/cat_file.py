import os, sys, zlib
from commands.utils import find_gitlite_repo

class fileAttributes:
	def __init__(self, type, size, body):
		self.type = type
		self.size = size
		self.body = body

def read_file(object):
	path = os.path.join(find_gitlite_repo(), 'objects', object[:2], object[2:])
	with open(path, 'rb') as f:
		data = zlib.decompress(f.read()).decode()
	null_index = data.find('\x00')
	return fileAttributes(data[:data.find(' ')], data[data.find(' ') + 1:null_index], data[null_index:])


def cat_file(args):
	try:
		fileObject = read_file(args.object)
		if args.object_type is not None:
			if args.type or args.size or args.print:
				raise Exception('You cannot define a type and an option at the same time.')
			print(fileObject.body)
		else:
			if not args.type and not args.size and not args.print:
				raise Exception('You have to specify either a type or an option.')
			elif args.type:
				print(fileObject.type)
			elif args.size:
				print(fileObject.size)
			else:
				print(fileObject.body)
	except Exception as e:
		print(f'Error: {e}')
		sys.exit(1)