from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol():
	name: str
	
	def __repr__(self):
		return "Symbol(" + repr(self.name) + ")"

@dataclass()
class Vector():
	lst: list
	
	def __init__(self, iterable):
		self.lst = list(iterable)
	
	def __iter__(self):
		return iter(self.lst)
	
	def __getitem__(self, key):
		return self.lst[key]
	
	def __setitem__(self, key, val):
		self.lst[key] = val
	
	def __len__(self):
		return len(self.lst)
	
	def __repr__(self):
		return "Vector(" + repr(self.lst) + ")"