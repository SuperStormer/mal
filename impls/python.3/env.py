class EnvError(KeyError):
	__str__ = Exception.__str__

class Env():
	def __init__(self, outer, data=None):
		self.outer = outer
		if data:
			self.data = data
		else:
			self.data = {}
	
	def __getitem__(self, key):
		try:
			
			return self.data[key]
		except KeyError:
			try:
				return self.outer[key]
			except TypeError:
				raise EnvError(f"{key.name!r} not found")
	
	def __setitem__(self, key, value):
		self.data[key] = value
	
	def __contains__(self, value):
		return value in self.data or value in self.outer
	
	def __repr__(self):
		return f"Env(outer={self.outer!r},data={self.data!r})"