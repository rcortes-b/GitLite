import sys, argparse
from messages import *

def init():
	print('Init thiss siuuu')

def status():
	print('Status thiss siuuu')

def main():
	if len(sys.argv) < 2:
		no_args_msg()
		sys.exit(1)
	parser = argparse.ArgumentParser(description="A minimal git implementation")
	commands = parser.add_subparsers(dest="commands", required=True)
	init_command = commands.add_parser('init')
	init_command.set_defaults(func=init)
	status_command = commands.add_parser('status')
	status_command.set_defaults(func=status)
	args = parser.parse_args()
	args.func()

if __name__ == "__main__":
	main()