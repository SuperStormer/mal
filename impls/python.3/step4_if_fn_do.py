#!/usr/bin/env python3
import itertools
import readline  # pylint: disable=unused-import
import sys

from core import core
from env import Env
from mal_types import Symbol, Vector
from pretty_print import pretty_print
from reader import read_str

global_env = Env(None, {Symbol(k): v for k, v in core.items()})

def read(inp: str):
	return read_str(inp)

def eval_(ast, env):
	if isinstance(ast, list):
		if ast:
			if ast[0] == Symbol("def!"):
				val = eval_(ast[2], env)
				env[ast[1]] = val
				return val
			elif ast[0] == Symbol("let*"):
				new_env = Env(env)
				# for loop b/c each def can depend on prev defs
				for key, value in zip(ast[1][::2], ast[1][1::2]):
					new_env[key] = eval_(value, new_env)
				return eval_(ast[2], new_env)
			elif ast[0] == Symbol("if"):
				result = eval_(ast[1], env)
				if result is not None and result is not False:  # then
					return eval_(ast[2], env)
				elif len(ast) >= 4:  # else
					return eval_(ast[3], env)
				else:  # no else clause
					return None
			elif ast[0] == Symbol("fn*"):
				
				def func(*args):
					binds = itertools.zip_longest(ast[1], args)
					data = {}
					for bind, expr in binds:
						if bind == Symbol("&"):  # varargs
							key, val = next(binds)
							if val:
								data[key] = [expr, val] + [arg for _, arg in binds]
							elif expr:  # 1 arg special case
								data[key] = [expr]
							else:  # 0 args special case
								data[key] = []
							break
						else:
							data[bind] = expr
					new_env = Env(env, data)
					return eval_(ast[2], new_env)
				
				return func
			elif ast[0] == Symbol("do"):
				return [eval_(el, env) for el in ast[1:]][-1]
			else:
				return eval_(ast[0], env)(*eval_ast(ast[1:], env))
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
	return pretty_print(inp, True)

def rep(inp: str):
	return print_(eval_(read(inp), global_env))

def main():
	while True:
		try:
			inp = input("user> ")
			print(rep(inp))
		except (EOFError, KeyboardInterrupt):
			print()
			break
		except Exception as e:
			print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
	main()
