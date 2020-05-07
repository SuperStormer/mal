from mal_types import Symbol,Vector


class Reader():
	def __init__(self, inp: str):
		self.tokens = self.tokenize(inp)
		self.pos = 0
	def tokenize(self, inp: str):
		tokens = []
		for line in inp.split("\n"):
			i = 0
			
			while i < len(line):
				x = line[i]
				if x.isspace() or x == ",":
					i += 1
				elif x == "~" and line[i + 1] == "@":
					tokens.append("~@")
					i += 2
				elif x in "[]{}()'`~^@":
					tokens.append(x)
					i += 1
				elif x == '"':
					i += 1
					chars = ""
					escaped = False
					try:
						while (x := line[i]) != '"' or escaped:
							if x == "\\" and not escaped:
								escaped = True
							else:
								escaped = False	
							chars += x
							i += 1
					except IndexError:
						raise SyntaxError("unbalanced double quote")
					i+=1			
					tokens.append('"' + chars + '"')
				elif x == ";":
					break
				else:
					chars = ""
					try:
						while (x := line[i]) not in "[]{}('\"`,;)" and not x.isspace():
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
		if x=="(":
			return self.read_list(")",list)
		elif x=="[":
			return self.read_list("]",Vector)
		else:
			return self.read_atom()
	def read_list(self,end_char,type_):
		self.pos += 1
		lst = []
		try:
			while self.peek() != end_char:
				lst.append(self.read_form())
		except IndexError:
			raise SyntaxError("unbalanced parentheses")
		self.pos += 1
		return type_(lst)
	def read_atom(self):
		x = self.next()
		try:
			return int(x)
		except ValueError:
			pass
		if x[0] == '"':
			return x[1:-1].replace('\\"','"').replace('\\n','\n').replace('\\\\','\\')
		return Symbol(x)

	def peek(self):
		return self.tokens[self.pos]
	def next(self):
		self.pos += 1
		return self.tokens[self.pos - 1]