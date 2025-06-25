import os, sys, zlib
from commands.utils.utils import find_gitlite_repo

class fileAttributes:
	def __init__(self, type, size, body):
		self.type = type
		self.size = size
		self.body = body

def parse_tree(data):
	pos = 0
	while pos < len(data):
		space = data.index(b' ', pos)
		mode = data[pos:space].decode()
		pos = space + 1

		null = data.index(b'\x00', pos)
		path = data[pos:null].decode()
		pos = null + 1

		sha = data[pos:pos+20].hex()
		pos += 20
		obj_type = 'tree' if mode == '040000' else 'blob'
		print(f"{mode} {obj_type} {sha} {path}")

def read_file(object_id):
	path = os.path.join(find_gitlite_repo(), 'objects', object_id[:2], object_id[2:])
	with open(path, 'rb') as f:
		raw = zlib.decompress(f.read())

	null_index = raw.find(b'\x00')
	header = raw[:null_index].decode()
	obj_type, size = header.split(' ')
	body = raw[null_index + 1:]

	return fileAttributes(obj_type, size, body)

def cat_file(args):
	try:
		fileObject = read_file(args.object)
		if args.object_type is not None:
			if args.type or args.size or args.print:
				raise Exception('You cannot define a type and an option at the same time.')
			if args.object_type == 'tree':
				if fileObject.type != 'tree':
					raise Exception('Requested type with object type don\'t match')
				parse_tree(fileObject.body)
			elif args.object_type == 'blob':
				if fileObject.type != 'blob':
					raise Exception('Requested type with object type don\'t match')
				print(fileObject.body.decode())
		else:
			if not args.type and not args.size and not args.print:
				raise Exception('You have to specify either a type or an option.')
			elif args.type:
				print(fileObject.type)
			elif args.size:
				print(fileObject.size)
			else:
				if fileObject.type == 'tree':
					parse_tree(fileObject.body)
				elif fileObject.type == 'blob':
					print(fileObject.body.decode())
				else:
					print('This will be a commit')
	except Exception as e:
		print(f'Error: {e}')
		sys.exit(1)