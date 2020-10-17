from espn_api.football import League
import csv

myQBs = []
myRBs = []
myWRs = []
myTEs = []
myDSTs = []
myKs = []
myFLEX = []
def findTopPlayers(link): #scrapes data from fantasypros.com to get top players in each position
    players = []
    with open(link) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        for row in csv_reader:
            split = row[1].split(" ")
            players.append(split[0] + " " + split[1])
        return players

    
            


def replacable(player,freeAgencyList,positionArray):
    playerName = player.name
    try:
        rankOfPlayer = positionArray.index(playerName)
    except:
        return 
    for players in freeAgencyList:
        try:
            if positionArray.index(players.name) < rankOfPlayer:
                string = players.name +  " should replace " + playerName
                return string
        except:
             pass
        
    
#We have to account for the differences in naming conventions between ESPN and fantasy pros.

def replaceDSTs(topDSTs):
    for i in range(1,len(topDSTs)):
        defenseSwitch = {
        "Buffalo Bills" : "Bills D/ST",
        "San Francisco" : "49ers D/ST",
        'Pittsburgh Steelers' : "Steelers D/ST",
        'Baltimore Ravens' : "Ravens D/ST",
        'Kansas City' : "Chiefs D/ST",
        'Chicago Bears' : "Bears D/ST",
        'Tennessee Titans' : "Titans D/ST",
        'LosAngeles Rams' : "Rams D/ST",
        'New Orleans' : "Saints D/ST",
        'Tampa Bay' : "Buccaneers D/ST",
        'Philadelphia Eagles': "Eagles D/ST",
        'Indianapolis Colts' : "Colts D/ST",
        'Arizona Cardinals' : "Cardinals D/ST",
        'Seattle Seahawks' : "Seahawks D/ST",
        'New England' : "Patriots D/ST",
        'Green Bay' : "Packers D/ST",
        "Washington Football" : "Washington D/ST",
        'Dallas Cowboys' : "Cowboys D/ST",
        'Minnesota Vikings' : "Vikings D/ST",
        'Denver Broncos' : "Broncos D/ST",
        'Cleveland Browns' : "Browns D/ST",
        'Cincinnati Bengals' : "Bengals D/ST",
        'Miami Dolphins' : "Dolphins D/ST",
        'NewYork Giants' : "Giants D/ST",
        'LosAngeles Chargers' : "Chargers D/ST",
        'NewYork Jets' : "Jets D/ST",
        'Las Vegas' : "Raiders D/ST",
        'Detroit Lions' : "Lions D/ST",
        'Jacksonville Jaguars' : "Jaguars D/ST",
        'Atlanta Falcons' : "Falcons D/ST",
        'Carolina Panthers' : "Panthers D/ST",
        'Houston Texans' : "Texans D/ST" 
    } #switch statement for using similar naming conventions
        topDSTs[i] = defenseSwitch[topDSTs[i]]  
    return topDSTs
        


def positionReplacable(changablePlayers,freeAgencyList,positionArray):
    output = ""
    for i in range(len(changablePlayers)):
        value = replacable(changablePlayers[i],freeAgencyList,positionArray)
        if value != None:
            output += value + ","
    return output

def setPositions(roster): #Add players to different position arrays
    for player in roster:
        if player.position == 'QB':
            myQBs.append(player)
        elif player.position == 'RB':
            myRBs.append(player)
        elif player.position == 'WR':
            myWRs.append(player)
        elif player.position == 'TE':
            myTEs.append(player)
        elif player.position == 'D/ST':
            myDSTs.append(player)
        else:
            myKs.append(player)

def topPositions(yourPlayers, bestPlayers):
    names = []
    for players in yourPlayers:
        names.append(players.name)
    ranks = ""
    for i in range(len(bestPlayers)):
        if bestPlayers[i] in names:
            ranks += bestPlayers[i] + ","
    return ranks + "/"

    
    
def getLeagueData(league_ID,espn_s2,swid,teamName):
    topQBs = findTopPlayers('csvfiles\QB.csv')
    topWRs = findTopPlayers('csvfiles\WR.csv')
    topRBs = findTopPlayers('csvfiles\RB.csv')
    topTEs = findTopPlayers('csvfiles\TE.csv')
    topDSTs = findTopPlayers('csvfiles\DST.csv')
    topKs = findTopPlayers('csvfiles\K.csv')
    topFLEX = findTopPlayers('csvfiles\FLEX.csv')
    replaceDSTs(topDSTs)
    #Gets the league from ESPN
    year = 2020 
    league = League(league_ID,year, espn_s2,swid)

    #gets my team and my roster
    for i in range(len(league.teams)):
        if league.teams[i].team_name == teamName:
            myTeam = league.teams[i]
    myRoster = myTeam.roster

    #Assigns different players to each position
    setPositions(myRoster)
    freeQBs = league.free_agents(size=20,position='QB')
    freeRBs = league.free_agents(size=75,position='RB')
    freeWRs = league.free_agents(size=75,position='WR')
    freeTEs = league.free_agents(size=40,position='TE')
    freeDSTs = league.free_agents(size=20,position='D/ST')
    freeKs = league.free_agents(size=20,position='K')
    myFLEX = myRBs
    myFLEX.extend(myWRs)
    myFLEX.extend(myTEs)
    
    total = ""
    total = topPositions(myQBs,topQBs) + topPositions(myRBs,topRBs) + topPositions(myWRs,topWRs) + topPositions(myTEs,topTEs) + topPositions(myFLEX,topFLEX) + topPositions(myDSTs,topDSTs) + topPositions(myKs,topKs) + "|"
    total += positionReplacable(myQBs,freeQBs,topQBs) +  positionReplacable(myRBs,freeRBs,topRBs) + positionReplacable(myWRs,freeWRs,topWRs) + positionReplacable(myTEs,freeTEs,topTEs) +positionReplacable(myDSTs,freeDSTs,topDSTs) + positionReplacable(myKs,freeKs,topKs)
    if len(total) == 0:
        total = "There are no better players on the free agency. "
    return total[0:len(total)-1]
    

