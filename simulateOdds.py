#!/usr/bin/python

import http.client
import urllib.parse
import re
import random
import math


oddsTable = {}
resultsTable = {}


# Method to get the odds of team1 beating team2 from dolphinsim.com
def getOdds(team1, team2, loc=0) :
    params = urllib.parse.urlencode({'dir' : 'ncaa_mbb', 'tn1' : team1, 'loc' : loc, 'tn2' : team2, 'submit':'Calculate'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", 'Referer':'http://dolphinsim.com/ratings/nhl/'}

    conn = http.client.HTTPConnection("dolphinsim.com")
    conn.request("POST", "/cgi-bin/del/ratings/wpredict", params, headers)
    response = conn.getresponse()

    lines = response.readlines()
    conn.close()
    for line in lines :
        l = line.decode('utf-8')
        if "WIN ODDS" in l :
            #print(l)
            odd= re.search('WIN ODDS = (.*)\%', l, re.IGNORECASE).group(1)
            break

    chance = float(odd)/100.0
    return chance



# Get the teams in bracket order
def loadBracket(fileName = "bracket.csv") :
    games = []
    team1 = None
    team2 = None
    try :
        f = open(fileName, 'r')
        for line in f:
            line = line.strip()
            if team1 == None :
                team1 = line
            else :
                team2 = line
                games.append((team1, team2))
                team1 = None
                team2 = None
    finally :
        f.close()
    return(games)


def playRound(games) :
    winners = []
    for aGame in games :
        team1 = aGame[0]
        team2 = aGame[1]
        gameKey = "%s-%s"%(team1, team2)
        if (gameKey in oddsTable) :
            odds = oddsTable[gameKey]
        else :
            odds = getOdds(team1, team2)
            oddsTable[gameKey] = odds
        #print("%s beats %s: %5.3f" % (team1, team2, odds))

        if random.random() < odds :
            winners.append(team1)
        else :
            winners.append(team2)
    return winners


def makeGames(winners) :
    games = []
    team1 = None
    team2 = None
    for t in winners :
        if team1 is None :
            team1 = t
        else :
            team2 = t
            games.append((team1, team2))
            team1 = None
            team2 = None
    return games


def oneSimulation(games) :
    index = 0
    while len(games) >= 1 :
        winners = playRound(games)
        for w in winners :
            resultsTable[w][index] += 1
        #print(winners)
        games = []
        if len(winners) > 1 :
            games = makeGames(winners)
        index += 1
        #print(resultsTable)
    return winners[0]


def setUpResults(games) :
    numGames = len(games)
    numRounds = int(math.log(numGames)/math.log(2) + 1)
    for g in games :
        resultsTable[g[0]] = [0] * numRounds
        resultsTable[g[1]] = [0] * numRounds



# Main Method
if __name__ == "__main__" :
    # Get the teams in bracket order
    firstGames = loadBracket()
    setUpResults(firstGames)

    games = firstGames
    #print(games)
    
    # Simulate the appropriate number of times
    numSim = 1000
    for x in range(0, numSim) :
        print("\rSimulation %d of %d" % (x+1, numSim), end='')
        champ = oneSimulation(games)
        #print(champ)
    #print(resultsTable)
    print()

    for team in resultsTable :
        results = resultsTable[team]
        print("%s\t%5.1f\t%5.1f\t%5.1f\t%5.1f" % (team.ljust(20), results[0]/numSim*100, results[1]/numSim*100, results[2]/numSim*100, results[3]/numSim*100))
