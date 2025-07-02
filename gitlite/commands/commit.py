import os, sys, time, zlib, hashlib
from commands.utils.utils import find_gitlite_repo, get_all_files, get_author
from commands.utils.objects import hash_tree
from commands.index import *

#tree 1f57a06c9ec667811fbc952bbc7bd55140b03e48
#parent 2e77efbee42aa7279b06f7d2d29f023403c304d5
#author rcortes-b <raulcortes.dev@gmail.com> 1751020076 +0200
#committer rcortes-b <raulcortes.dev@gmail.com> 1751020076 +0200
#\n--------------
#add sha1 index fix and 2/3 status parts done


def commit(args):
	path = find_gitlite_repo(False)
	a, e = get_author()
	if a is None and e is None:
		a = 'default'
		e = 'default@defaultmail.com'
	author = f"{a} {e} {int(time.time())} {time.strftime('%z')}"
	tree_data, _ = hash_tree(path)
	path = os.path.join(path, '.gitlite/refs/heads/main')
	prev_commit_sha1 = None
	if not os.path.exists(path):
		os.makedirs(os.path.dirname(path), exist_ok=True)
		prev_commit_sha1 = '0000000000000000000000000000000000000000'
	else:
		with open(path, 'r') as f:
			prev_commit_sha1 = f.read().replace('\n', '')

	commit_content = []
	commit_content.append(f"tree {tree_data['sha1']}")
	commit_content.append(f'parent {prev_commit_sha1}')
	commit_content.append(f'author {author}')
	commit_content.append(f'committer {author}')
	commit_content.append('')
	commit_content.append(args.message)
	body = "\n".join(commit_content)
	print(body)
	
	header = f"commit {len(body)}\0"
	full_data = (header + body).encode()
	sha1 = hashlib.sha1(full_data).hexdigest()

	with open(path, 'w') as f:
		f.write(f'{sha1}\n')
	path = os.path.join(find_gitlite_repo(), 'objects', sha1[:2], sha1[2:])
	if not os.path.exists(path):
		os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'wb') as f:
		f.write(zlib.compress(full_data))
		
	