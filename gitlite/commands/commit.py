import os, time, zlib, hashlib, sys
from .utils.utils import find_gitlite_repo, get_all_files, get_author
from .utils.objects import hash_tree
from .index import *

#tree 1f57a06c9ec667811fbc952bbc7bd55140b03e48
#parent 2e77efbee42aa7279b06f7d2d29f023403c304d5
#author rcortes-b <raulcortes.dev@gmail.com> 1751020076 +0200
#committer rcortes-b <raulcortes.dev@gmail.com> 1751020076 +0200
#\n--------------
#add sha1 index fix and 2/3 status parts done

def no_index_msg():
	print('On branch master\n')
	print('Initial commit\n')
	print("nothing to commit (create/copy files and use \"gitlite add\" to track)")
	sys.exit(0)

def no_changes_msg():
	print('On branch master')
	print('nothing to commit, working tree clean')
	sys.exit(0)

def check_if_are_changes(prev_commit_sha1, sha1):
	if '0000000000000000000000000000000000000000' == prev_commit_sha1:
		return True
	path = os.path.join(find_gitlite_repo(), 'objects', prev_commit_sha1[:2], prev_commit_sha1[2:])
	with open(path, 'rb') as f:
		data = zlib.decompress(f.read())
	data = data[data.find(b'\x00') +1:].decode()
	sha = data[5:45]
	if sha == sha1:
		return False
	return True


def commit(args):
	path = find_gitlite_repo(False)
	if path is None:
		print('fatal: not gitlite repository found')
		sys.exit(1)
	elif not os.path.exists(os.path.join(path, '.gitlite/index')):
		no_index_msg()
	a, e = get_author()
	if a is None and e is None:
		a = 'default'
		e = 'default@defaultmail.com'
	author = f"{a} {e} {int(time.time())} {time.strftime('%z')}"
	tree_data, _ = hash_tree()
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
	
	header = f"commit {len(body)}\0"
	full_data = (header + body).encode()
	sha1 = hashlib.sha1(full_data).hexdigest()
	if check_if_are_changes(prev_commit_sha1, tree_data['sha1']) is False:
		no_changes_msg()
	with open(path, 'w') as f:
		f.write(f'{sha1}\n')
	path = find_gitlite_repo()
	if path is None:
		print('fatal: not gitlite repository found')
		sys.exit(1)
	path = os.path.join(path, 'objects', sha1[:2], sha1[2:])
	if not os.path.exists(path):
		os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'wb') as f:
		f.write(zlib.compress(full_data))
	print('commit has been succesfully created, modifications saved')
	print('commit sha is:', sha1)
		
	