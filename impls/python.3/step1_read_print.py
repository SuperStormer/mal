#!/usr/bin/env python3
import readline  # pylint: disable=unused-import
import sys

from pretty_print import pretty_print
from reader import Reader, ReaderError

def read(inp: str):
	return Reader(inp).read_form()

def eval_(inp: str):
	return inp

def print_(inp: str) -> str:
	return pretty_print(inp)

def rep(inp: str):
	return print_(eval_(read(inp)))

def main():
	while True:
		try:
			inp = input("user> ")
			print(rep(inp))
		except ReaderError as e:
			print("SyntaxError:", e)
		except EOFError:
			print()
			break

if __name__ == "__main__":
	main()
