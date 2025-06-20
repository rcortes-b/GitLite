import os

def init(args):
	prog_name = ".gitlite"
	try:
		if args.repo_name is not None:
			os.makedirs(args.repo_name)
		else:
			args.repo_name = '.'
		os.makedirs(os.path.join(args.repo_name, prog_name))
		for name in ['objects', 'refs', 'refs/heads']:
			os.mkdir(os.path.join(args.repo_name, prog_name, name))
		print('Repository has been created succesfully!')
	except:
		print('Repository could not be created because it already exists!')