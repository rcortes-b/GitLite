import sys
from args import parse_args
from messages import *

def main():
	if len(sys.argv) < 2:
		usage_msg()
		sys.exit(1)
	args = parse_args()
	args.func(args)

if __name__ == "__main__":
	main()