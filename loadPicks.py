import math

class Picks :

    name = None
    startPts = 0
    currentPts = 0
    roundPicks = []
    wins = 0
    seconds = 0
    historyPts = 0
    historyGms = 0
    historyMax = 0
    historyMin = 999

    def __init__(self, name, pts) :
        self.name = name
        self.startPts = int(pts)
        self.currentPts = int(self.startPts)
        self.roundPicks = []
        self.wins = 0
        self.seconds = 0
        self.historyPts = 0
        self.historyGms = 0

    def addPicks(self,roundNum, picks) :
        #print(len(self.roundPicks))
        while len(self.roundPicks) < roundNum :
            self.roundPicks.append([])
            #print(len(self.roundPicks))
        self.roundPicks[roundNum-1] = picks
        #print((self.roundPicks))

    def getPicks(self, roundNum) :
        return self.roundPicks[roundNum - 1]

    def addPts(self, pts) :
        self.currentPts += pts

    def getPts(self) :
        return self.currentPts

    def resetTeam(self) :
        self.historyPts += self.currentPts
        self.historyGms += 1
        if self.currentPts > self.historyMax :
            self.historyMax = self.currentPts
        if self.currentPts < self.historyMin :
            self.historyMin = self.currentPts
        self.currentPts = self.startPts

    def avgPts(self) :
        return self.historyPts / self.historyGms

    def __str__(self) :
        returnString = "%s \t %d \t %d \t %5.1f \t %d \t %d"%(self.name.ljust(10), self.wins, self.seconds, self.avgPts(), self.historyMax, self.historyMin)
        #returnString = "%s - %d - Picks: %s "%(self.name, self.currentPts, self.roundPicks)
        #for p in self.roundPicks :
            #print(p)
            #returnString += p
        return returnString



class Group :

    name = None
    teams = []

    def __init__(self, name, rounds, fileName="picks.csv") :
        self.name = name
        self.teams = self.loadPicks(rounds, fileName)

    def loadPicks(self, rounds, fileName="picks.csv") :
        numPicks = 2^rounds - 1
        personArray = []
        try :
            f = open(fileName, "r")
            for line in f:
                picks = line.strip().split(',')
                team = picks[0]
                currentPts = picks[1]
                person = Picks(team, currentPts)

                totCount = 2
                for i in range(0, rounds) :
                    thisRound = []
                    for j in range(0, 2**(rounds - (i+1))) :
                        #print("Round: %d  i: %d   j Range: %d" % (rounds, i, 2**(rounds-(i+1))))
                        #print("%d - %d - %s" % (i, j, picks[totCount]))
                        thisRound.append(picks[totCount])
                        totCount += 1
                    #print(thisRound)
                    person.addPicks(i+1, thisRound)
                #print(person)
                personArray.append(person)
        finally :
            f.close()
        return personArray


    def simplePrint(self, winners, index) :
        roundNum = int(6 - math.log(len(winners))/math.log(2))
        value = int(2 ** (roundNum - 1))
        for t in self.teams :
            #print(t)
            #print(index+1)
            tPicks = t.getPicks(index+1)
            #print("Picks")
            #print(tPicks)
            #print("Winners")
            #print(winners)
            for i in range(0, len(tPicks)) :
                if winners[i] == tPicks[i] :
                    t.addPts(value)


    def determineWinner(self) :
        maxPts = 0
        maxTeam = None
        self.teams.sort(key=lambda x: x.getPts(), reverse=True)
        self.teams[0].wins += 1
        self.teams[1].seconds += 1
        return self.teams[0]



    def resetGroup(self) :
        for t in self.teams :
            t.resetTeam()


    def endSimulation(self) :
        self.determineWinner()
        self.resetGroup()


    def __str__(self) :
        returnString = self.name + "\n"
        returnString += "=" * 30 + "\n"
        self.teams.sort(key=lambda x: (x.wins, x.seconds, x.avgPts()), reverse=True)
        for t in self.teams :
            returnString += str(t) + "\n"
        return returnString



if __name__ == "__main__" :
    #group = loadPicks(4)
    group = Group(4)
    for p in group.teams :
        print(p.getPicks(2))
        #print(p)
