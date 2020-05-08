#!/usr/bin/env python3
import readline  # pylint: disable=unused-import
import sys

from core import core
from env import Env
from mal_types import Function, Symbol, Vector
from pretty_print import pretty_print
from reader import read_str


def read(inp: str):
	return read_str(inp)

def eval_(ast, env):
	while True:
		if isinstance(ast, list):
			if ast:
				ast = macro_expand(ast, env)
				if isinstance(ast, list):
					if ast[0] == Symbol("def!"):
						val = eval_(ast[2], env)
						env[ast[1]] = val
						return val
					elif ast[0] == Symbol("let*"):
						env = Env(env)
						# for loop b/c each def can depend on prev defs
						for key, value in zip(ast[1][::2], ast[1][1::2]):
							env[key] = eval_(value, env)
						ast = ast[2]
						continue
					elif ast[0] == Symbol("if"):
						result = eval_(ast[1], env)
						if result is not None and result is not False:  # then
							ast = ast[2]
						elif len(ast) >= 4:  # else
							ast = ast[3]
							continue
						else:  # no else clause
							return None
					elif ast[0] == Symbol("fn*"):
						return Function(ast[2], ast[1], env, eval_)
					elif ast[0] == Symbol("do"):
						eval_ast(ast[1:-1], env)
						ast = ast[-1]
						continue
					elif ast[0] == Symbol("quote"):
						return ast[1]
					elif ast[0] == Symbol("quasiquote"):
						ast = quasiquote(ast[1])
						continue
					elif ast[0] == Symbol("defmacro!"):
						val = eval_(ast[2], env)
						val.is_macro = True
						env[ast[1]] = val
						return val
					elif ast[0] == Symbol("macroexpand"):
						return macro_expand(ast[1], env)
					elif ast[0] == Symbol("try*"):
						try:
							return eval_(ast[1], env)
						except Exception as e:
							if ast[2][0] != Symbol("catch*"):
								print("Warning: catch* not found", file=sys.stderr)
							env = Env(env)
							env[ast[2][1]] = str(e)
							return eval_(ast[2][2], env)
					
					else:
						fn = eval_(ast[0], env)
						if isinstance(fn, Function):
							env = fn.bind_args(eval_ast(ast[1:], env))
							ast = fn.body
							continue
						return fn(*eval_ast(ast[1:], env))
				else:
					return eval_ast(ast, env)
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

def quasiquote(ast):
	if not isinstance(ast, (list, Vector)) or len(ast) == 0:
		return [Symbol("quote"), ast]
	elif ast[0] == Symbol("unquote"):
		return ast[1]
	elif isinstance(ast[0], (list, Vector)) and ast[0][0] == Symbol("splice-unquote"):
		return [Symbol("concat"), ast[0][1], quasiquote(ast[1:])]
	else:
		return [Symbol("cons"), quasiquote(ast[0]), quasiquote(ast[1:])]

def is_macro_call(ast, env):
	try:
		return env[ast[0]].is_macro
	except (AttributeError, IndexError, KeyError, TypeError):
		return False

def macro_expand(ast, env):
	while is_macro_call(ast, env):
		macro = env[ast[0]]
		ast = macro(*ast[1:])
	return ast

def print_(inp: str) -> str:
	return pretty_print(inp, True)

def rep(inp: str):
	return print_(eval_(read(inp), global_env))

#setup global env
global_env = Env(None, {Symbol(k): v for k, v in core.items()})
global_env[Symbol("eval")] = lambda ast: eval_(ast, global_env)
global_env[Symbol("*ARGV*")] = sys.argv[2:]
rep('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\\nnil)")))))')
rep(
	"(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))"
)

def main():
	
	if len(sys.argv) > 1:
		rep(f"(load-file \"{sys.argv[1]}\")")
		return
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
