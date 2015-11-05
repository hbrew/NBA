#!/bin/python
from lineup import Lineup

# Sort the players by position
def getPositions(players):
	pgs = []
	pfs = []
	sgs = []
	sfs = []
	cs = []
	for key in players:
		pos = players[key].POS
		if pos == 'PG':
			pgs.append(players[key])
		elif pos == 'PF':
			pfs.append(players[key])
		elif pos == 'SG':
			sgs.append(players[key])
		elif pos == 'SF':
			sfs.append(players[key])
		elif pos == 'C':
			cs.append(players[key])
	return pgs, pfs, sgs, sfs, cs

# Check each possible lineup and save the score
def getOptions(pgs, pfs, sgs, sfs, cs):
	budget = 60
	options = []
	for l in range(len(pgs)):
		for m in range(1,len(pgs)):
			if l >= m:
				continue
			for n in range(len(pfs)):
				for o in range(1,len(pfs)):
					if n >= o:
						continue
					for p in range(len(sgs)):
						for q in range(1,len(sgs)):
							if p >= q:
								continue
							for r in range(len(sfs)):
								for s in range(1,len(sfs)):
									if r >= s:
										continue
									for t in range(len(cs)):
										cost = (
											pgs[l].SALARY + 
											pgs[m].SALARY + 
											pfs[n].SALARY + 
											pfs[o].SALARY + 
											sgs[p].SALARY + 
											sgs[q].SALARY + 
											sfs[r].SALARY + 
											sfs[s].SALARY + 
											cs[t].SALARY
										)
										if cost < budget:
											score = (
												pgs[l].SCORE + 
												pgs[m].SCORE + 
												pfs[n].SCORE + 
												pfs[o].SCORE + 
												sgs[p].SCORE + 
												sgs[q].SCORE + 
												sfs[r].SCORE + 
												sfs[s].SCORE + 
												cs[t].SCORE
											)
											names = (
												pgs[l].NAME, 
												pgs[m].NAME, 
												pfs[n].NAME, 
												pfs[o].NAME, 
												sgs[p].NAME, 
												sgs[q].NAME, 
												sfs[r].NAME, 
												sfs[s].NAME, 
												cs[t].NAME
											)
											options.append((names, score, cost))
	return options



def run(players):
	pgs, pfs, sgs, sfs, cs = getPositions(players)
	n = 5 # limited samples for speed
	options = getOptions(pgs[0:n], pfs[0:n], sgs[0:n], sfs[0:n], cs[0:n])
	scores = [option[1] for option in options]
	best = max(scores)
	bestIdx = [n for n,m in enumerate(scores) if m == best]
	return [options[n] for n in bestIdx]

