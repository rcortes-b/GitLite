import os

def usage_msg():
	print('Usage: gitlite <options> <command> <command_options> <...>\n\n' \
	'Options:\n' \
	'\t-h, --help\n'\
	'\t-v, --verbose\n' \
	'\nCommands:\n' \
	'\tinit\n' \
	'\thash_object\n'\
	'\tcommit')

def find_gitlite_repo(root=True):
	try:
		path = os.path.abspath('.')
		while path != os.path.dirname(path):
			if os.path.isdir(os.path.join(path, '.gitlite')):
				if root is False:
					return path
				return os.path.join(path, '.gitlite')
			path = os.path.dirname(path)
		raise Exception('fatal: not gitlite repository found')
	except Exception as e: 
		print('{e}')
