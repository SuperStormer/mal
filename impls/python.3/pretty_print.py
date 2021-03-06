import itertools

from mal_types import Symbol, Vector

def pretty_print(obj, print_readably=True):
	if obj is None:
		return "nil"
	elif isinstance(obj, Symbol):
		return obj.name
	elif isinstance(obj, list):
		return "(" + " ".join(pretty_print(el, print_readably) for el in obj) + ")"
	elif isinstance(obj, Vector):
		return "[" + " ".join(pretty_print(el, print_readably) for el in obj) + "]"
	elif isinstance(obj, str):
		if print_readably:
			return '"%s"' % obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
		else:
			return str(obj)
	elif isinstance(obj, bool):
		return str(obj).lower()
	elif isinstance(obj, dict):
		return "{" + " ".join(
			itertools.chain.from_iterable(
			(pretty_print(key, print_readably), pretty_print(value, print_readably))
			for key, value in obj.items()
			)
		) + "}"
	return str(obj)
