import os, sys, zlib
from .utils.utils import find_gitlite_repo

class fileAttributes:
	def __init__(self, type, size, body):
		self.type = type
		self.size = size
		self.body = body

def parse_tree(data):
	pos = 0
	lines = []
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
		lines.append({'obj_type': obj_type,
					  'sha': sha,
					  'path': path,
					  'mode': mode})
	return lines

def read_file(object_id):
	path = find_gitlite_repo()
	if path is None:
		print('fatal: not gitlite repository found')
		sys.exit(1)
	path = os.path.join(path, 'objects', object_id[:2], object_id[2:])
	with open(path, 'rb') as f:
		raw = zlib.decompress(f.read())

	null_index = raw.find(b'\x00')
	header = raw[:null_index].decode()
	obj_type, size = header.split(' ')
	body = raw[null_index + 1:]

	return fileAttributes(obj_type, size, body)

def cat_file(args):
	tree_data = None
	try:
		fileObject = read_file(args.object)
		if args.object_type is not None:
			if args.type or args.size or args.print:
				raise Exception('You cannot define a type and an option at the same time.')
			if args.object_type == 'tree':
				if fileObject.type != 'tree':
					raise Exception('Requested type with object type doesn\'t match')
				tree_data = parse_tree(fileObject.body)
			elif args.object_type == 'blob':
				if fileObject.type != 'blob':
					raise Exception('Requested type with object type doesn\'t match')
				print(fileObject.body.decode(), end='')
			else:
				if fileObject.type != 'commit':
					raise Exception('Requested type with object type doesn\'t match')
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
					tree_data = parse_tree(fileObject.body)
				elif fileObject.type == 'blob':
					print(fileObject.body.decode(), end='')
				else:
					print(fileObject.body.decode())
		if tree_data is not None:
			for data in tree_data:
				print(f"{data['mode']} {data['obj_type']} {data['sha']}\t{data['path']}")
	except Exception as e:
		print(f'Error: {e}')
		sys.exit(1)