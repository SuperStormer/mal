from mal_types import Symbol

def pretty_print(obj):
	if obj is ...:
		return ""
	elif isinstance(obj, Symbol):
		return obj.name
	elif isinstance(obj, list):
		return "(" + " ".join(map(pretty_print, obj)) + ")"
	elif isinstance(obj, str):  # from https://stackoverflow.com/a/1676170/7941251
		return '"%s"' % repr(obj)[1:-1].replace('"', r'\"')
	return str(obj)
