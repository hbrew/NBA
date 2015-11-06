#!/bin/python

### Class for players

class Player:
	# Fanduel score multipliers
	scoring = [
		3,	#fg3pt
		2,	#fg2pt
		1,	#ft
		1.2,	#rbd
		1.5,	#ast
		2,	#blk
		2,	#stl
		-1	#tov
	]

	def __init__(self, name, pos, salary, fg3pt, fg2pt, ft, rbd, ast, blk, stl, tov):
		self.NAME = name
		self.POS = pos
		self.SALARY = salary
		self.FG3PT = fg3pt # (attempted, percentage)
		self.FG2PT = fg2pt # (attempted, percentage)
		self.FT = ft
		self.RBD = rbd
		self.AST = ast
		self.BLK = blk
		self.STL = stl
		self.TOV = tov

	def setOpponent(self, opp):
		self.OPP = opp

	def calcScore(self):
		fg3pt = self.FG3PT[0]*(self.FG3PT[1] + self.OPP.FG3PT_DIFF)
		fg2pt = self.FG2PT[0]*(self.FG2PT[1] + self.OPP.FG2PT_DIFF)
		ft = self.FT
		rbd = self.RBD*(1 + self.OPP.RBD)
		ast = self.AST*(1 + self.OPP.AST)
		blk = self.BLK*(1 + self.OPP.BLK)
		stl = self.STL*(1 + self.OPP.STL)
		tov = self.TOV*(1 + self.OPP.TOV)
		cats = [fg3pt, fg2pt, ft, rbd, ast, blk, stl, tov]
		self.SCORE = sum([a*b for a,b in zip(cats, self.scoring)])
		self.EFF = self.SCORE / self.SALARY




