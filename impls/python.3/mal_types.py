from dataclasses import dataclass
import itertools
import env

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

class Function():
	def __init__(self, body, params, env, eval_, is_macro=False):
		self.body = body
		self.params = params
		self.env = env
		self.eval_ = eval_
		self.is_macro = is_macro
	
	def bind_args(self, args):
		binds = itertools.zip_longest(self.params, args)
		data = {}
		for bind, expr in binds:
			if bind == Symbol("&"):  # varargs
				key, val = next(binds)
				if val:
					data[key] = [expr, val] + [arg for _, arg in binds]
				elif expr:  # 1 arg special case
					data[key] = [expr]
				else:  # 0 args special case
					data[key] = []
				break
			else:
				data[bind] = expr
		return env.Env(self.env, data)
	
	def __call__(self, *args):
		
		return self.eval_(self.body, self.bind_args(args))

@dataclass
class Atom():
	def __init__(self, val):
		self.val = val
	
	def __str__(self):
		return f"(atom {self.val})"

class MalException(Exception):
	def __init__(self, val):
		super().__init__(val)
		self.val = val
	
	def __str__(self):
		return str(self.val)

@dataclass
class Keyword:
	name: str
	
	def __str__(self):
		return ":" + self.name
