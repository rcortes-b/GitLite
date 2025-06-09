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

def find_gitlite_repo(path='.'):
    path = os.path.abspath(path)

    while path != os.path.dirname(path):
        if os.path.isdir(os.path.join(path, '.gitlite')):
            return os.path.join(path, '.gitlite')
        path = os.path.dirname(path)

    return None
