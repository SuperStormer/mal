from mal_types import Keyword, Symbol, Vector,hash_map

class ReaderError(Exception):
	pass

class Reader():
	def __init__(self, inp: str):
		self.tokens = self.tokenize(inp)
		self.pos = 0
	def tokenize(self, inp: str):
		tokens = []
		i = 0
		while i < len(inp):
			x = inp[i]
			if x.isspace() or x == ",":
				i += 1
			elif x == "~" and inp[i + 1] == "@":
				tokens.append("~@")
				i += 2
			elif x in "[]{}()'`~^@":
				tokens.append(x)
				i += 1
			elif x == '"': #string
				i += 1
				chars = ""
				escaped = False
				try:
					while (x := inp[i]) != '"' or escaped:
						if x == "\\" and not escaped:
							escaped = True
						else:
							escaped = False	
						chars += x
						i += 1
				except IndexError:
					raise ReaderError("unbalanced double quote")
				i+=1
				tokens.append('"' + chars + '"')
			elif x == ";":
				try:
					i+=1
					while (x:=inp[i]) != '\n':
						i+=1
					i+=1
				except IndexError:
					pass	
			else: #keywords
				chars = ""
				try:
					while (x := inp[i]) not in "[]{}('\"`,;)" and not x.isspace():
						chars += x
						i += 1
				except IndexError:
					pass		
				tokens.append(chars)
		return tokens
	
	def read_form(self):
		if not self.tokens:
			return None
		x = self.peek()
		if x == "(":
			return self.read_list(")",list)
		elif x == "[":
			return self.read_list("]",Vector)
		elif x== "{":
			return self.read_list("}",hash_map)	
		elif x == "@": #atom deref
			return self.macro("deref")
		elif x== "'":
			return self.macro("quote")
		elif x== "`":
			return self.macro("quasiquote")
		elif x== "~":
			return self.macro("unquote")
		elif x== "~@":
			return self.macro("splice-unquote")	
		elif x== "^":
			self.pos += 1
			val = self.read_form()
			fn = self.read_form()
			return [Symbol("with-meta"), fn,val]					
		else:
			return self.read_atom()
	def read_list(self,end_char,type_):
		self.pos += 1
		lst = []
		try:
			while self.peek() != end_char:
				lst.append(self.read_form())
		except IndexError:
			raise ReaderError("unbalanced parentheses")
		self.pos += 1
		return type_(lst)
	def read_atom(self):
		x = self.next()
		try:
			return int(x)
		except ValueError:
			pass
		if x[0] == '"': # strings
			string = ""
			escaped = False
			for c in x[1:-1]:
				if escaped:
					if c == "n":
						string += "\n"
					else:
						string += c
					escaped = False
				elif c == "\\":
					escaped = True
				else:
					string += c
			return string
		if x[0]==":": #keywords
			return Keyword(x[1:])
		if x == "true":
			return True
		if x== "false":
			return False
		if x=="nil":
			return None
		return Symbol(x)
	def macro(self, func: str):
		self.pos += 1
		return [Symbol(func), self.read_form()]	
	def peek(self):
		return self.tokens[self.pos]
	def next(self):
		self.pos += 1
		return self.tokens[self.pos - 1]
def read_str(inp:str):
	return Reader(inp).read_form()