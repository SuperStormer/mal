#!/usr/bin/env python3
import readline  # pylint: disable=unused-import

def read(inp: str):
	return inp

def eval_(inp: str):
	return inp

def print_(inp: str):
	return inp

def rep(inp: str):
	return print_(eval_(read(inp)))

def main():
	try:
		while True:
			inp = input("user> ")
			print(rep(inp))
	except EOFError:
		print("")

if __name__ == "__main__":
	main()