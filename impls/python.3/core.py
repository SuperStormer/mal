import itertools
import operator
import time

from mal_types import Atom, Keyword, MalException, Symbol, Vector, hash_map, Function
from pretty_print import pretty_print
from reader import read_str

def _eq(x, y):
	if isinstance(x, dict) and isinstance(y, dict):
		return len(x) == len(y) and all(
			_eq(a[1], b[1]) for a, b in zip(sorted(x.items()), sorted(y.items()))
		)
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

def _dissoc(hm: dict, *args):
	hm2 = hm.copy()
	for key in args:
		hm2.pop(key, None)
	return hm2

def _readline(prompt: str):
	try:
		return input(prompt)
	except EOFError:
		return None

def _meta(fn):
	raise NotImplementedError

def _with_meta(fn, val):
	raise NotImplementedError

def _conj(seq, *args):
	if isinstance(seq, list):
		return list(reversed(args)) + seq
	return Vector(seq.lst + list(args))

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
	"seq": lambda x: list(x) if x else None,
	"conj": _conj,
	#hash maps
	"assoc": lambda hm, *args: {
	**hm,
	**hash_map(args)
	},
	"dissoc": _dissoc,
	"get": lambda hm, key: None if hm is None else hm.get(key, None),
	"contains?": lambda hm, key: key in hm,
	"keys": lambda hm: list(hm.keys()),
	"vals": lambda hm: list(hm.values()),
	#atoms
	"deref": lambda x: x.val,
	"reset!": _reset,
	"swap!": _swap,
	#printing
	"pr-str": lambda *args: " ".join(pretty_print(x, True) for x in args),
	"str": lambda *args: "".join(pretty_print(x, False) for x in args),
	"prn": lambda *args: print(" ".join(pretty_print(x, True) for x in args)),
	"println": lambda *args: print(" ".join(pretty_print(x, False) for x in args)),
	#ctors
	"list": lambda *args: list(args),
	"vector": lambda *args: Vector(args),
	"symbol": Symbol,
	"keyword": lambda x: x if isinstance(x, Keyword) else Keyword(x),
	"hash-map": lambda *args: hash_map(args),
	"atom": Atom,
	#predicates
	"list?": lambda x: isinstance(x, list),
	"vector?": lambda x: isinstance(x, Vector),
	"sequential?": lambda x: isinstance(x, (list, Vector)),
	"symbol?": lambda x: isinstance(x, Symbol),
	"keyword?": lambda x: isinstance(x, Keyword),
	"map?": lambda x: isinstance(x, dict),
	"atom?": lambda x: isinstance(x, Atom),
	"string?": lambda x: isinstance(x, str),
	"number?": lambda x: isinstance(x, int) and not isinstance(x, bool),
	"fn?": lambda x: not x.is_macro if isinstance(x, Function) else callable(x),
	"macro?": lambda x: isinstance(x, Function) and x.is_macro,
	"nil?": lambda x: x is None,
	"true?": lambda x: x is True,
	"false?": lambda x: x is False,
	#io
	"read-string": read_str,
	"slurp": _slurp,
	"readline": _readline,
	#misc
	"throw": _throw,
	"apply": lambda fn, *args: fn(*itertools.chain(args[:-1], args[-1])),
	"time-ms": lambda: time.time_ns() //
	1000000,  # from https://stackoverflow.com/a/56394660/7941251
	"meta": _meta,
	"with-meta": _with_meta
}
