import os
from .index import read_index
from .utils.utils import get_all_files, find_gitlite_repo
from .utils.objects import hash_blob

def do_cached(index):
	for entry in index:
		print(entry['path'])

def do_stage(index):
	for entry in index:
		print(f"{entry['fields']['mode']} {entry['fields']['sha1']} 0\t{entry['path']}")

def do_deleted(index):
	all_files = get_all_files()
	if all_files is None:
		return
	for entry in index:
		found = False
		for files in all_files:
			if files == entry['path']:
				found = True
				break
		if found is False:
			print(entry['path'])

def do_modified(index):
	all_files = get_all_files()
	if all_files is None:
		return
	for entry in index:
		for files in all_files:
			if files == entry['path']:
				if entry['fields']['sha1'] != hash_blob(os.path.join(find_gitlite_repo(False), entry['path']), False):
					print(entry['path'])

def do_others(index):
	root_path = find_gitlite_repo(False)
	all_files = []
	for rootdir, dirname, filenames in os.walk(root_path):
		for filename in filenames:
			found = False
			f = os.path.join(rootdir.replace(root_path, ''), filename).replace('/', '', 1)
			if index is not None:
				for entry in index:
					if entry['path'] == f:
						found = True
						continue
			if found is False:
				print(f)

def ls_files(args):
	if not (args.cached or args.stage or args.deleted or args.modified or args.others):
		args.cached = True
	index = read_index()
	if args.others:
		do_others(index)
	elif index is None:
		return
	elif args.cached:
		do_cached(index)
	elif args.stage:
		do_stage(index)
	elif args.deleted:
		do_deleted(index)
	elif args.modified:
		do_modified(index)
