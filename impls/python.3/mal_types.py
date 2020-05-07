from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol():
	name: str
	
	def __repr__(self):
		return "Symbol(" + repr(self.name) + ")"
