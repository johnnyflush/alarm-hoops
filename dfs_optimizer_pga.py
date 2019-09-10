# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 08:41:38 2019

@author: admin
"""

from pydfs_lineup_optimizer import get_optimizer, Site, Sport, CSVLineupExporter
import pandas
import math
import csv
class JohnLineupExporter(object):
    def __init__(self, lineups):
        # type: (Iterable[Lineup]) -> None
        self.lineups = lineups

    @staticmethod
    def render_player(player):
        # type: (LineupPlayer) -> str
        result = player.full_name  # type: str
        if player.id:
            result += '(%s)' % player.id
        return result

    def export(self, filename, render_func=None):
        # type: (str, Callable[[LineupPlayer], str]) -> None
        raise NotImplementedError


class JohnCSVLineupExporter(JohnLineupExporter):
    def export(self, filename, render_func=None):
        # type: (str, Callable[[LineupPlayer], str]) -> None
        with open(filename, 'a') as csvfile:
            lineup_writer = csv.writer(csvfile, delimiter=',')
            for index, lineup in enumerate(self.lineups):
                if index == 0:
                    header = [player.lineup_position for player in lineup.lineup]
                    header.extend(('Budget', 'FPPG'))
                    lineup_writer.writerow(header)
                row = [(render_func or self.render_player)(player) for player in lineup.lineup]
                row.append(str(lineup.salary_costs))
                row.append(str(lineup.fantasy_points_projection))
                lineup_writer.writerow(row)

#put in right format
filelocation = r"C:\Users\admin\Downloads\DKSalaries_pga.csv"
resultlocation = r"C:\Users\admin\Downloads\DKresults.csv"
lineups = 3

df = pandas.read_csv(filelocation)
new_cols=['Position','Name + ID', 'Name', 'ID', 'Roster Position', 'Salary', 'Game Info','TeamAbbrev', 'AvgPointsPerGame'] #MLB
df.rename(columns=dict(zip(df.columns[0:8], new_cols)),inplace=True)
df.to_csv(filelocation, index=False)


player_include = ['Justin Rose','Jason Kokrak']
player_exclude = [] #,'Aaron Rai','Kodai Ichihara','Philip Eriksson','Webb Simpson']

#LOOP THORUGH HIGH TOTAL TEAMS TO STACK
for i in range((1+len(player_include))*(1+len(player_exclude))):
    #sports:  GOLF, BASEBALL
    optimizer = get_optimizer(Site.DRAFTKINGS, Sport.GOLF)
    optimizer.load_players_from_csv(filelocation)
    
    # to lock in players
    if (i % (1+len(player_include))) > 0:       
        player = optimizer.get_player_by_name(player_include[-1+(i % (1+len(player_include)))]) # find player with specified name in your optimizer
        #second_player = optimizer.get_player_by_id('12864605')  # find player with player id
        optimizer.add_player_to_lineup(player) # lock this player in lineup
        #optimizer.add_player_to_lineup(second_player)
    if (math.floor(i / (1+len(player_include))) > 0):
        player = optimizer.get_player_by_name(player_exclude[math.floor(-1+(i / (1+len(player_include))))])
        optimizer.remove_player(player)
        #optimizer.restore_player(player)
        
    if i == 0:
        exporter = CSVLineupExporter(optimizer.optimize(lineups))
    else:
        exporter = JohnCSVLineupExporter(optimizer.optimize(lineups))
    exporter.export(resultlocation) 
   
    
#%%    
for lineup in optimizer.optimize(n=1):
    print(lineup)
    print(lineup.players)  # list of players
    print(lineup.fantasy_points_projection)
    print(lineup.salary_costs) 
#%%
#put in right format
from pydfs_lineup_optimizer import get_optimizer, Site, Sport, CSVLineupExporter
import pandas
import math
import csv
filelocation = r"C:\Users\admin\Downloads\DKSalaries_pga.csv"
resultlocation = r"C:\Users\admin\Downloads\DKresults.csv"
lineups = 50

df = pandas.read_csv(filelocation)
new_cols=['Position','Name + ID', 'Name', 'ID', 'Roster Position', 'Salary', 'Game Info','TeamAbbrev', 'AvgPointsPerGame'] #MLB
df.rename(columns=dict(zip(df.columns[0:8], new_cols)),inplace=True)
df.to_csv(filelocation, index=False)
#sports:  GOLF, BASEBALL
optimizer = get_optimizer(Site.DRAFTKINGS, Sport.GOLF)
optimizer.load_players_from_csv(filelocation)
exporter = CSVLineupExporter(optimizer.optimize(lineups))
exporter.export(resultlocation) 