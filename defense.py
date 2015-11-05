#!/bin/python

### Class for Defenses

class Defense:
	def __init__(self, team_id, fg3pt, fg2pt, rbd, ast, blk, stl, tov):
		self.TEAM = team_id
		self.FG3PT_DIFF = fg3pt
		self.FG2PT_DIFF = fg2pt
		self.RBD = rbd
		self.AST = ast
		self.BLK = blk
		self.STL = stl
		self.TOV = tov

