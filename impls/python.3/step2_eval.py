#!/usr/bin/env python3
import readline  # pylint: disable=unused-import
import sys
import operator
from mal_types import Symbol, Vector
from pretty_print import pretty_print
from reader import Reader
environ = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv}

def read(inp: str):
	return Reader(inp).read_form()

def eval_(ast):
	if isinstance(ast, list):
		if ast:
			evaled_list = eval_ast(ast)
			return evaled_list[0](*evaled_list[1:])
		else:
			return ast
	return eval_ast(ast)

def eval_ast(ast):
	if isinstance(ast, Symbol):
		return environ[ast.name]
	elif isinstance(ast, list):
		return list(map(eval_, ast))
	elif isinstance(ast, Vector):
		return Vector(map(eval_, ast))
	else:
		return ast

def print_(inp: str) -> str:
	return pretty_print(inp)

def rep(inp: str):
	return print_(eval_(read(inp)))

def main():
	while True:
		try:
			inp = input("user> ")
			print(rep(inp))
		except EOFError:
			print()
			break
		except Exception as e:
			print(e, file=sys.stderr)

if __name__ == "__main__":
	main()
