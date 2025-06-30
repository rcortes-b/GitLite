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
		gitconfig = []
		gitconfig.append('[user]')
		gitconfig.append(f"\t\temail = {args.email if args.email else 'default@defaultmail.com'}")
		gitconfig.append(f"\t\tname = {args.author if args.author else 'default'}")
		with open(os.path.join(args.repo_name, '.gitconfig'), 'w') as f:
			f.write('\n'.join(gitconfig))
		print('Repository has been created succesfully!')
	except:
		print('Repository could not be created because it already exists!')