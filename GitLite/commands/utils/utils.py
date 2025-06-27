import os, sys

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
		sys.exit(1)

def get_all_files(root_path=find_gitlite_repo(False)):
	all_files = []
	ignored_files = get_ignored_files(root_path)
	for rootdir, dirname, filenames in os.walk(root_path):
		for filename in filenames:
			f = os.path.join(rootdir.replace(root_path, ''), filename).replace('/', '', 1)
			if path_ignored(f, ignored_files, root_path) is False:
				all_files.append(f)
	#for file in all_files:
	#	print(file)
	return all_files

def get_ignored_files(path=find_gitlite_repo(False)):
	if not os.path.exists(os.path.join(path, '.gitliteignore')):
		return
	lines = []
	with open(os.path.join(path, '.gitliteignore'), 'r') as f:
		for line in f:
			lines.append(line.strip())
	lines.append(".gitlite/")
	return lines

def path_ignored(file, ignored_list, path):
	for ignored_file in ignored_list:
		if ignored_file == '':
			continue
		is_directory =  True if ignored_file[-1] == '/' else False
		if is_directory is False:
			if os.path.exists(os.path.join(path, ignored_file)) and file == ignored_file:
				#print('IGNORED: ', file)
				return True
		else:
			i = file.find(ignored_file)
			if i > -1:
				#print('IGNORED: ', file)
				return True
	return False
			
def dir_in_list(list_object, value):
	for obj in list_object:
		if value == obj or (value + '/') == obj:
			return True
	return False

def file_in_list(list_object, value):
	for file in list_object:
		if file == value:
			return True
	return False
			