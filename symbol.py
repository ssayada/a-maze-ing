class Symbol:
	def __init__(self, name: str):
		self.name = name
		if self.name == "A":
			self.H_WALL = "━"
			self.V_WALL = "┃"
			self.FILL = " "
			self.DOT = "╋"
			self.ENTRY = "#"
			self.EXIT = "$"
			self.PATH = "%"
		elif self.name == "B":
			self.H_WALL = "─"
			self.V_WALL = "│"
			self.FILL = " "
			self.DOT = "┼"
			self.ENTRY = "●"
			self.EXIT = "◎"
			self.PATH = "•"
		elif self.name == "C":
			self.H_WALL = "═"
			self.V_WALL = "║"
			self.FILL = " "
			self.DOT = "╬"
			self.ENTRY = "◉"
			self.EXIT = "○"
			self.PATH = "∙"
