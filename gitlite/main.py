import sys, os
from .args import parse_args
from .commands.utils.utils import usage_msg

def main():
	if len(sys.argv) < 2:
		usage_msg()
		sys.exit(1)
	args = parse_args()
	args.func(args) if len(sys.argv) > 2 else args.func()


if __name__ == "__main__":
	main()