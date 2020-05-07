from mal_types import Symbol, Vector

def pretty_print(obj):
	if obj is None:
		return ""
	elif isinstance(obj, Symbol):
		return obj.name
	elif isinstance(obj, list):
		return "(" + " ".join(map(pretty_print, obj)) + ")"
	elif isinstance(obj, Vector):
		return "[" + " ".join(map(pretty_print, obj)) + "]"
	elif isinstance(obj, str):
		return '"%s"' % repr(obj)[1:-1].replace('"', r'\"')
	return str(obj)
