from commands.utils.objects import hash_tree
def write_tree():
	sha1 = hash_tree()
	print(sha1)