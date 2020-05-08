import operator
from pretty_print import pretty_print
from mal_types import Vector, Atom
from reader import read_str
import itertools

def _eq(x, y):
	if isinstance(x, (list, Vector)) and isinstance(y, (list, Vector)):
		return len(x) == len(y) and all(_eq(a, b) for a, b in zip(x, y))
	return x == y

def _slurp(filename: str):
	with open(filename, "r") as f:
		return f.read()

def _reset(atom: Atom, val):
	atom.val = val
	return val

def _swap(atom: Atom, fn, *args):
	atom.val = fn(atom.val, *args)
	return atom.val

core = {
	#basic
	"+": operator.add,
	"-": operator.sub,
	"*": operator.mul,
	"/": operator.floordiv,
	"=": _eq,
	"<": operator.lt,
	"<=": operator.le,
	">": operator.gt,
	">=": operator.ge,
	"not": lambda x: x is None or x is False,
	#lists
	"list": lambda *args: list(args),
	"list?": lambda x: isinstance(x, list),
	"empty?": lambda lst: len(lst) == 0,
	"count": lambda x: 0 if x is None else len(x),
	#sequence
	"cons": lambda x, seq: [x] + list(seq),
	"concat": lambda *args: list(itertools.chain.from_iterable(args)),
	#printing
	"pr-str": lambda *args: " ".join(pretty_print(x, True) for x in args),
	"str": lambda *args: "".join(pretty_print(x, False) for x in args),
	"prn": lambda *args: print(" ".join(pretty_print(x, True) for x in args)),
	"println": lambda *args: print(" ".join(pretty_print(x, False) for x in args)),
	#files
	"read-string": read_str,
	"slurp": _slurp,
	#atoms
	"atom": Atom,
	"atom?": lambda x: isinstance(x, Atom),
	"deref": lambda x: x.val,
	"reset!": _reset,
	"swap!": _swap
}
