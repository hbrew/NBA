#!/bin/python

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
	return pgs, sgs, sfs, pfs, cs

# Sort players by points/cost
def sortEff(players):
	return sorted(players, key=lambda x: x.EFF, reverse=True)

# Check each possible lineup and save the score
def getOptions(pgs, pfs, sgs, sfs, cs):
	budget = 60
	options = []
	for l in range(len(pgs)):
		for m in range(1,len(pgs)):
			if l >= m:
				continue
			for n in range(len(sgs)):
				for o in range(1,len(sgs)):
					if n >= o:
						continue
					for p in range(len(sfs)):
						for q in range(1,len(sfs)):
							if p >= q:
								continue
							for r in range(len(pfs)):
								for s in range(1,len(pfs)):
									if r >= s:
										continue
									for t in range(len(cs)):
										cost = (
											pgs[l].SALARY + 
											pgs[m].SALARY + 
											sgs[n].SALARY + 
											sgs[o].SALARY + 
											sfs[p].SALARY + 
											sfs[q].SALARY + 
											pfs[r].SALARY + 
											pfs[s].SALARY + 
											cs[t].SALARY
										)
										if cost < budget:
											score = (
												pgs[l].SCORE + 
												pgs[m].SCORE + 
												sgs[n].SCORE + 
												sgs[o].SCORE + 
												sfs[p].SCORE + 
												sfs[q].SCORE + 
												pfs[r].SCORE + 
												pfs[s].SCORE + 
												cs[t].SCORE
											)
											names = (
												pgs[l].NAME, 
												pgs[m].NAME, 
												sgs[n].NAME, 
												sgs[o].NAME, 
												sfs[p].NAME, 
												sfs[q].NAME, 
												pfs[r].NAME, 
												pfs[s].NAME, 
												cs[t].NAME
											)
											options.append((names, score))
	return options



def run(players):
	pgs, sgs, sfs, pfs, cs = getPositions(players)
	pgs = sortEff(pgs)
	pfs = sortEff(pfs)
	sgs = sortEff(sgs)
	sfs = sortEff(sfs)
	cs = sortEff(cs)
	m = 0
	n = 9 # limited samples for speed
	options = getOptions(pgs[m:n], sgs[m:n], sfs[m:n], pfs[m:n], cs[m:n])
	scores = [option[1] for option in options]
	## Return single best team
	#best = max(scores)
	#bestIdx = [n for n,m in enumerate(scores) if m == best]
	#return [options[n] for n in bestIdx]
	## Return a set of the best teams
	options = sorted(options, key=lambda x: x[1], reverse=True)
	return options[0:5]

