import itertools
import operator

from mal_types import Atom, MalException, Vector, Symbol
from pretty_print import pretty_print
from reader import read_str

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

def _throw(val):
	raise MalException(val)

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
	#sequence
	"empty?": lambda seq: len(seq) == 0,
	"count": lambda x: 0 if x is None else len(x),
	"cons": lambda x, seq: [x] + list(seq),
	"concat": lambda *args: list(itertools.chain.from_iterable(args)),
	"nth": lambda seq, i: seq[i],
	"first": lambda seq: None if seq is None or not seq else seq[0],
	"rest": lambda seq: [] if seq is None or not seq else seq[1:],
	"map": lambda fn, seq: list(map(fn, seq)),
	#printing
	"pr-str": lambda *args: " ".join(pretty_print(x, True) for x in args),
	"str": lambda *args: "".join(pretty_print(x, False) for x in args),
	"prn": lambda *args: print(" ".join(pretty_print(x, True) for x in args)),
	"println": lambda *args: print(" ".join(pretty_print(x, False) for x in args)),
	#files
	"read-string": read_str,
	"slurp": _slurp,
	#atoms
	"deref": lambda x: x.val,
	"reset!": _reset,
	"swap!": _swap,
	#ctors and predicates
	"list": lambda *args: list(args),
	"list?": lambda x: isinstance(x, list),
	"vector": lambda *args: Vector(args),
	"vector?": lambda x: isinstance(x, Vector),
	"symbol": Symbol,
	"symbol?": lambda x: isinstance(x, Symbol),
	"atom": Atom,
	"atom?": lambda x: isinstance(x, Atom),
	"nil?": lambda x: x is None,
	"true?": lambda x: x is True,
	"false?": lambda x: x is False,
	"throw": _throw,
	"apply": lambda fn, *args: fn(*itertools.chain(args[:-1], args[-1]))
}
