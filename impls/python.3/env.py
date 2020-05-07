from mal_types import Symbol

class Env():
	def __init__(self, outer, data={}):
		self.outer = outer
		self.data = {Symbol(k): v for k, v in data.items()}
	
	def __getitem__(self, key):
		try:
			return self.data.get(key) or self.outer[key]
		except TypeError:
			raise KeyError(f"{key.name!r} not found in environment")
	
	def __setitem__(self, key, value):
		self.data[key] = value
	
	def __contains__(self, value):
		return value in self.data or value in self.outer
