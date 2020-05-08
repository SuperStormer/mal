import operator
from pretty_print import pretty_print
from mal_types import Vector

def _eq(x, y):
	if isinstance(x, (list, Vector)) and isinstance(y, (list, Vector)):
		return len(x) == len(y) and all(_eq(a, b) for a, b in zip(x, y))
	return x == y

core = {
	"+": operator.add,
	"-": operator.sub,
	"*": operator.mul,
	"/": operator.floordiv,
	"list": lambda *args: list(args),
	"list?": lambda obj: isinstance(obj, list),
	"empty?": lambda lst: len(lst) == 0,
	"count": lambda obj: 0 if obj is None else len(obj),
	"=": _eq,
	"<": operator.lt,
	"<=": operator.le,
	">": operator.gt,
	">=": operator.ge,
	"not": lambda obj: obj is None or obj is False,
	"pr-str": lambda *args: " ".join(pretty_print(obj, True) for obj in args),
	"str": lambda *args: "".join(pretty_print(obj, False) for obj in args),
	"prn": lambda *args: print(" ".join(pretty_print(obj, True) for obj in args)),
	"println": lambda *args: print(" ".join(pretty_print(obj, False) for obj in args)),
}
