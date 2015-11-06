import scrape, lineups

def output(data):
	#print players
	print('[ %s, %s, %s, %s, %s, %s, %s, %s, %s ]' % data[0])
	print("Projected Score: %0.2f" % data[1])


players = scrape.getData()
best = lineups.run(players)
for data in best:
	output(data)
	print('')