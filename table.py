from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QCalendarWidget, QLabel
from PyQt5.QtCore import QDate
import sys, requests, http.client, json, datetime

#Configuring API connection.
connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': '1dbe4b92009b4405b32134ece04b6ec2' }

#Getting the starting date of the current Premier League season in progress.
connection.request('GET', '/v2/competitions/PL/standings', None, headers )
currentSeason = json.loads(connection.getresponse().read().decode()) 
currentLeagueStartDate = currentSeason['season']['startDate']

#Getting a dictionary of teams in the current Premier league season.
connection.request('GET', '/v2/competitions/PL/teams', None, headers )
premierLeagueTeams = json.loads(connection.getresponse().read().decode())

#Getting a dictionary of finished matches played so far in the Premier League.
connection.request('GET', '/v2/competitions/PL/matches/?status=FINISHED', None, headers )
matchesPlayed = json.loads(connection.getresponse().read().decode())

def getTeamStatistics():
    '''
    Returns an array of arrays, each containing statistics of each Premier League team and their
    progress in the current eason.
    '''
    teamStatistics = []

    #Adding an array to teamStatistics for each team containing statistics relevant to their placement
    #in the table.
    for team in premierLeagueTeams['teams']:
        teamStatistics.append(

                         [ team['name'], #Team name - index 0
                                      0, #Played games - index 1
                                      0, #Won - index 2
                                      0, #Drawn - index 3
                                      0, #Lost - index 4
                                      0, #Goal difference - index 5
                                      0, #Points - index 6
                                    
                         ]

                         )

    return teamStatistics


def sortData(startDate, teamStats):
    '''
    Parameters: startDate is a string representing a date in the form "yyyy-MM-dd".

                teamStats is an array containing arrays of the form 
                [team name, played games, won, drawn, lost, goal difference, points]
                relevant to each team

    This function return a dictionary of the form 
    {'Team':[], 'MP':[], 'W':[], 'D':[], 'L':[], 'GD':[], 'Points':[]}, with each key containing
    statistics only from or after the startDate for each team found in teamStats. 
    '''
    for match in matchesPlayed['matches']:
        
        i = 0

        if datetime.datetime.strptime(match['utcDate'][0:10], "%Y-%m-%d") >= datetime.datetime.strptime(startDate, "%Y-%m-%d"):
            
            for team in teamStats: 
                #Updating stastistics for each team in teamStats from the matches played statistics
                #from the API.
                if team[0] == match['homeTeam']['name']:
                   teamStats[i][1] += 1
                   if match['score']['winner'] == 'HOME_TEAM':
                      teamStats[i][2] += 1
                      teamStats[i][6] += 3
                   elif match['score']['winner'] == 'DRAW':    
                      teamStats[i][3] += 1
                      teamStats[i][6] += 1
                   else:
                      teamStats[i][4] += 1  
                   teamStats[i][5] += match['score']['fullTime']['homeTeam']   
                   teamStats[i][5] -= match['score']['fullTime']['awayTeam']

                elif team[0] == match['awayTeam']['name']:
                    teamStats[i][1] += 1
                    if match['score']['winner'] == 'AWAY_TEAM':
                        teamStats[i][2] += 1
                        teamStats[i][6] += 3
                    elif match['score']['winner'] == 'DRAW':    
                        teamStats[i][3] += 1
                        teamStats[i][6] += 1
                    else:
                        teamStats[i][4] += 1
                    teamStats[i][5] += match['score']['fullTime']['awayTeam']   
                    teamStats[i][5] -= match['score']['fullTime']['homeTeam']  

                i += 1

    #Sorting each team in teamStats primarily by points total, and then by goal difference.
    teamStats.sort(reverse = True, key = lambda l: (l[6], l[5]))  

    data = {'Team':[],
            'MP':[],
            'W':[],
            'D':[], 
            'L':[], 
            'GD':[], 
            'Points':[], 
            }

    #Transferring the sorted teamStats array to the data dictionary to be displayed in the table.
    for team in teamStats:
        data['Team'].append(team[0])
        data['MP'].append(str(team[1]))
        data['W'].append(str(team[2]))
        data['D'].append(str(team[3]))
        data['L'].append(str(team[4]))
        data['GD'].append(str(team[5]))
        data['Points'].append(str(team[6]))

    return data                  

#Creating an initial table data variable to be displayed upon application initialisation.
tableData = sortData(currentLeagueStartDate, getTeamStatistics())

class TableView(QTableWidget):
    def __init__(self, tableData, *args):
        QTableWidget.__init__(self, *args)

        #Table widget specifications.
        self.tableData = tableData
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setWindowTitle("Premier league table")

        #Window specifications.
        self.top = 100
        self.left = 100
        self.width = 880
        self.height = 490
        self.setGeometry(self.top, self.left, self.width, self.height)

        #Instructions specifications.
        instructionLabel = QLabel(self)
        instructionLabel.move(450, 40)
        instructionLabel.setText(
            '''                Instructions:

                Select an available date from the calendar to display a table 
                of Premier League results determined only from the selected date 
                until present.'''
            )
 
        #Date picker specifications.
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(500, 140)

        #Limiting date picker to dates from the beginning of the current season to now.
        max_date = QDate.fromString(datetime.datetime.now().strftime("%Y-%m-%d"), 'yyyy-MM-dd')
        min_date = QDate.fromString(currentLeagueStartDate, 'yyyy-MM-dd')
        cal.setMaximumDate(max_date)
        cal.setMinimumDate(min_date)

        #Changing data displayed in table to reflect information only from the selected date.
        cal.clicked[QDate].connect(lambda: self.changeData(cal.selectedDate().toString("yyyy-MM-dd")))
 
    def setData(self): 
        '''
        Sets initial data in the table for the all matches currently played 
        in the season upon application initialisation.
        '''
        horHeaders = []
        for n, key in enumerate(self.tableData.keys()):
            horHeaders.append(key)
            for m, item in enumerate(self.tableData[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

    def changeData(self, start):
        '''
        start is a string representing a date in the form "yyyy-MM-dd".
        Changes the data in the table to represent the league based on 
        statistics only from (and including) the date represented by 
        the start parameter.
        ''' 
        data = sortData(start, getTeamStatistics())
        horHeaders = []
        for n, key in enumerate(data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

def main(args):
    app = QApplication(args)
    table = TableView(tableData, 20, 7)
    table.show()
    sys.exit(app.exec_())
 
if __name__=="__main__":
    main(sys.argv)