#!/bin/python

###
### Scrape data from websites and organize it into classes
###

from lxml import html
import requests, json
from defense import Defense
from player import Player

## Relevant URLS ##
# Current Player Stats #
defenseURL = 'http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Opponent&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='
defenseFG3URL = 'http://stats.nba.com/stats/leaguedashptteamdefend?DefenseCategory=3+Pointers&LastNGames=0&LeagueID=00&Month=0&OpponentTeamID=0&PORound=0&PerMode=PerGame&Period=0&Season=2015-16&SeasonType=Regular+Season&TeamID=0'
defenseFG2URL = 'http://stats.nba.com/stats/leaguedashptteamdefend?DefenseCategory=2+Pointers&LastNGames=0&LeagueID=00&Month=0&OpponentTeamID=0&PORound=0&PerMode=PerGame&Period=0&Season=2015-16&SeasonType=Regular+Season&TeamID=0'
playerStatsURL = 'http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='

# 2014-15 stats #
# defenseURL = 'http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Opponent&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='
# defenseFG3URL = 'http://stats.nba.com/stats/leaguedashptteamdefend?DefenseCategory=3+Pointers&LastNGames=0&LeagueID=00&Month=0&OpponentTeamID=0&PORound=0&PerMode=PerGame&Period=0&Season=2014-15&SeasonType=Regular+Season&TeamID=0'
# defenseFG2URL = 'http://stats.nba.com/stats/leaguedashptteamdefend?DefenseCategory=2+Pointers&LastNGames=0&LeagueID=00&Month=0&OpponentTeamID=0&PORound=0&PerMode=PerGame&Period=0&Season=2014-15&SeasonType=Regular+Season&TeamID=0'
# playerStatsURL = 'http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='

# Dated line up #
#lineupURL = 'https://rotogrinders.com/lineups/nba?date=2015-11-05&site=fanduel'
# Current line up #
lineupURL = 'https://rotogrinders.com/lineups/nba?site=fanduel'

# Parse numeric salary from things like $8.2k
def parseSalary(salary):
	if len(salary) > 0:
		return float(salary[1:-1])
	else:
		return 0

# Rotogrinders uses . in abbreviations, nba doesn't
def parseName(name):
	return name.replace('.', '')

# Roto marks people who aren't playing with projected points of 0
def cleanLineup(names, pos, salaries, points):
	for n in reversed(range(len(points))):
		if points[n] == 0 or salaries[n] == 0:
			del names[n]
			del pos[n]
			del salaries[n]
			del points[n]
	return names, pos, salaries, points

# Roto lineup page isn't showing salaries, this pulls them from individual player pages
# This is much slower but may be necessary for making predictions hours before a game
def altSalaries(tree):
	profiles = tree.xpath('//a[@class="player-popup"]/@href')
	salaries = []
	for profile in profiles:
		parts = profile.split('-')
		playerId = parts[-1]
		url = 'https://rotogrinders.com/players/' + playerId + '/projection'
		page = requests.get(url)
		data = json.loads(page.text)
		if 'error' in data:
			salary = 100000
		else:
			salary = data['schedule']['data']['salaries']['collection'][0]['data']['salary']/1000.0
		salaries.append(salary)
	return salaries

# Get the lineup of players for tonights games
def getLineups():
	page = requests.get(lineupURL)
	tree = html.fromstring(page.text)
	positions = tree.xpath('//li[@class="player"]/@data-pos')
	salaries = tree.xpath('//li[@class="player"]/@data-salary')
	salaries = [parseSalary(s) for s in salaries]
	# salaries = altSalaries(tree)
	points = tree.xpath('//span[@class="fpts"]/text()')
	points = [float(p) for p in points]
	names = tree.xpath('//a[@class="player-popup"]/@title')
	names = [parseName(n) for n in names]
	return cleanLineup(names, positions, salaries, points)

# Get rid of players we don't have stats for
def removeUnknown(names, positions, salaries, points, data):
	for n in reversed(range(len(names))):
		if names[n] not in data:
			firstLast = names[n].split()
			if firstLast[0] not in data: # fuck you nene again
				del names[n]
				del positions[n]
				del salaries[n]
				del points[n]
	return names, positions, salaries, points

# Only keep stats of players playing
def removeUnused(targets, data, idx):
	for n in reversed(range(len(data))):
		val = data[n][idx];
		if val not in targets:
			if isinstance(val, int):
				del data[n]
			else:
				# necessary when checking names
				firstLast = [x.split(' ') for x in targets]
				if val not in [x[0] for x in firstLast]:
					del data[n]
				else: # fuck you nene
					for m in range(len(firstLast)):
						if val in firstLast[m][0]:
							data[n][1] = targets[m]
	return data

# Get opposing team of each player
# first find team of each player. Because of how the lineup is sorted,
# adjacent sets of teams will be playing each other
def getOpponents(names, data):
	teams = [[]]
	opps = []
	nTeams = 0
	for n in range(len(names)):
		team = [row[1] for row in data if names[n] in row]
		if len(teams[nTeams]) is 0:
			teams[nTeams].append(team[0])
		elif team[0] != teams[nTeams][0]:
			teams.append(team)
			nTeams = nTeams + 1
		else:
			teams[nTeams].append(team[0])
	n = 0
	nPlayers = 0
	prevTeam = 0
	for team in teams:
		n = n + 1
		if n % 2 is not 0:
			nPlayers = len(team)
			prevTeam = team[0]
			continue
		for m in range(nPlayers):
			opps.append(team[0])
		for m in range(len(team)):
			opps.append(prevTeam)
	return opps

# Scrape the player data
def getPlayerData(names):
	page = requests.get(playerStatsURL)
	data = json.loads(page.text)
	data = data['resultSets'][0]['rowSet']
	data = removeUnused(names, data, 1)
	return data
	
# Organize the stats from the data
def getPlayerStats(names, data):
	# stat indices in data
	fgm = 10
	fga = 11
	fg3m = 13
	fg3a = 14
	ftm = 16
	rbd = 21
	ast = 22
	tov = 23
	stl = 24
	blk = 25
	statsAll = []
	for name in names:
		stats = []
		n = [i for i,val in enumerate(data) if name in val]
		n = n[0]
		fg3prc = 0 if data[n][fg3m] == 0 else data[n][fg3m]/data[n][fg3a] # 3 points made / attempts
		fg3pt = (data[n][fg3a], fg3prc)
		fg2a = data[n][fga] - data[n][fg3a] # total - 3 pointers
		fg2m = data[n][fgm] - data[n][fg3m]
		fg2prc = 0 if fg2m == 0 else fg2m/fg2a
		fg2pt = (fg2a, fg2prc)
		stats.extend([
			fg3pt, 
			fg2pt, 
			data[n][ftm], 
			data[n][rbd], 
			data[n][ast], 
			data[n][blk], 
			data[n][stl], 
			data[n][tov]
		])
		statsAll.append(stats)
	return statsAll

# Opposing team stats
def getDefenseStats(opps):
	#indices for stats
	fg3_diff = 10
	fg2_diff = 10
	rbd = 18
	ast = 19
	tov = 20
	stl = 21
	blk = 22
	page = requests.get(defenseURL)
	page3 = requests.get(defenseFG3URL)
	page2 = requests.get(defenseFG2URL)
	data = json.loads(page.text)
	data = data['resultSets'][0]['rowSet']
	data3 = json.loads(page3.text)
	data3 = data3['resultSets'][0]['rowSet']
	data2 = json.loads(page2.text)
	data2 = data2['resultSets'][0]['rowSet']
	# Find the percent different from the average for each stat for modifying players
	rbd_sum = 0
	ast_sum = 0
	blk_sum = 0
	stl_sum = 0
	tov_sum = 0
	for team in data:
		rbd_sum += team[rbd]
		ast_sum += team[ast]
		blk_sum += team[blk]
		stl_sum += team[stl]
		tov_sum += team[tov]
	nTeams = len(data)
	rbd_avg = rbd_sum/nTeams
	ast_avg = ast_sum/nTeams
	blk_avg = blk_sum/nTeams
	stl_avg = stl_sum/nTeams
	tov_avg = tov_sum/nTeams
	data = removeUnused(opps, data, 0)
	data3 = removeUnused(opps, data3, 0)
	data2 = removeUnused(opps, data2, 0)
	
	statsAll = {}
	for opp in set(opps):
		stats = []
		n = [i for i,val in enumerate(data) if opp in val]
		n = n[0]
		n2 = [i for i,val in enumerate(data2) if opp in val]
		n2 = n2[0]
		n3 = [i for i,val in enumerate(data3) if opp in val]
		n3 = n3[0]
		stats.extend([
			data3[n3][fg3_diff],
			data2[n2][fg2_diff],
			data[n][rbd]/rbd_avg - 1,
			data[n][ast]/ast_avg - 1,
			data[n][blk]/blk_avg - 1,
			data[n][stl]/stl_avg - 1,
			data[n][tov]/tov_avg - 1
		])
		statsAll[opp] = stats
	# Most of these stats need to be normalized to the average of all teams
	return statsAll

# Store defense data in objects
def getDefenses(opps, stats):
	defenses = {}
	for opp in opps:
		defense = Defense(
			opp, 
			stats[opp][0],
			stats[opp][1],
			stats[opp][2],
			stats[opp][3],
			stats[opp][4],
			stats[opp][5],
			stats[opp][6]
		)
		defenses[opp] = defense
	return defenses

#store the player data in objects
def getPlayers(names, positions, salaries, stats, opps, defenses):
	players = {}
	for n in range(len(names)):
		player = Player(
			names[n],
			positions[n],
			salaries[n],
			stats[n][0],
			stats[n][1],
			stats[n][2],
			stats[n][3],
			stats[n][4],
			stats[n][5],
			stats[n][6],
			stats[n][7]
		)
		player.setOpponent(defenses[opps[n]])
		player.calcScore()
		players[names[n]] = player
	return players

# This runs first and calls everything else
def getData():
	names, positions, salaries, points = getLineups()
	data = getPlayerData(names)
	names, positions, salaries, points = removeUnknown(names, positions, salaries, points, [a[1] for a in data])
	stats = getPlayerStats(names, data)
	opps = getOpponents(names, [a[1:3] for a in data]) # passed list of names and team ids
	opps_stats = getDefenseStats(opps)

	defenses = getDefenses(opps, opps_stats)
	players = getPlayers(names, positions, salaries, stats, opps, defenses)

	return players
	

