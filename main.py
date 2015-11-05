import scrape, lineups

players = scrape.getData()
best = lineups.run(players)
print(best)