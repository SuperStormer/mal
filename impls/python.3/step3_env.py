#!/usr/bin/env python3
import readline  # pylint: disable=unused-import
import sys
import operator
from mal_types import Symbol, Vector
from pretty_print import pretty_print
from reader import Reader
from env import Env
global_env = Env(
	None, {
	"+": operator.add,
	"-": operator.sub,
	"*": operator.mul,
	"/": operator.floordiv,
	"def!": None,
	"let*": None
	}
)

def read(inp: str):
	return Reader(inp).read_form()

def eval_(ast, env):
	if isinstance(ast, list):
		if ast:
			#evaled_list = eval_ast(ast, env)
			if ast[0] == Symbol("def!"):
				val = eval_(ast[2], env)
				env[ast[1]] = val
				return val
			elif ast[0] == Symbol("let*"):
				env = Env(env)
				#TODO
			else:
				return env[ast[0]](*eval_ast(ast[1:], env))
		else:
			return ast
	else:
		return eval_ast(ast, env)

def eval_ast(ast, env):
	if isinstance(ast, Symbol):
		return env[ast]
	elif isinstance(ast, list):
		return [eval_(el, env) for el in ast]
	elif isinstance(ast, Vector):
		return Vector(eval_(el, env) for el in ast)
	else:
		return ast

def print_(inp: str) -> str:
	return pretty_print(inp)

def rep(inp: str):
	return print_(eval_(read(inp), global_env))

def main():
	while True:
		try:
			inp = input("user> ")
			print(rep(inp))
		except EOFError:
			print()
			break
		except Exception as e:
			e_type, e_value, _ = sys.exc_info()
			print(e_type.__name__ + ":", e_value, file=sys.stderr)

if __name__ == "__main__":
	main()
