# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 15:28:06 2018

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 11:23:26 2018

@author: admin
"""

#scraping odds
from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException 


###################################################

# Script to Run Program

###################################################

# Opens Chrome & goes to the Website (Must download chrome driver from the interwebs)

chrome_driver_path = r'C:\Users\admin\Downloads\chromedriver_win32\chromedriver.exe' #path of the driver you installed

browser = webdriver.Chrome(chrome_driver_path)

url_string = 'https://rotogrinders.com/projected-stats?site=draftkings&sport=nba'
browser.get(url_string)

"""
ids = browser.find_elements_by_xpath("//*[@id]")
for ii in ids:
    print(ii.get_attribute('id'))
"""

ml_info = browser.find_element_by_xpath('//*[contains(@id, "proj-stats")]')
ml_text = ml_info.text.strip()
#%%
#take out RankDiff whitespace
#PLTN_Start = ml_text.find('\nRankDiff\n')
#PLTN_End = ml_text.find('nSituation\n') 
#s = list(ml_text)
#s = s[0:PLTN_Start-1]+s[PLTN_End:]
#ml_text = "".join(s)
#
##replace missing values with |
#while ml_text.find('\n ') >= 0:
#    s = list(ml_text)
#    s[1+ml_text.find('\n ')] = '|'
#    ml_text = "".join(s)
#%%
Name_Start = ml_text.find('\nName\n')
Salary_Start = ml_text.find('\nSalary\n')
#carriage returns between Name_Start and Salary_Start should be number of players + 1 
Num_Players = [pos for pos, char in enumerate(ml_text[1+Name_Start:Salary_Start+2]) if char == '\n']
#create player list

PlayerList = []
for pIndex in range(len(Num_Players)-2):
    players = ml_text[Name_Start+Num_Players[pIndex]+2:1+Name_Start+Num_Players[pIndex+1]]
    PlayerList.append(players)
    
SalaryList = []
TeamList = []
PositionList = []
OppList = []
TotalList = []
MovementList = []
DvPList = []
DvPRankList = []
PMINList = []
PointsList = []
ValueList = []
Team_Start = ml_text.find('\nTeam\n')
Position_Start = ml_text.find('\nPosition\n')
Opp_Start = ml_text.find('\nOpp\n')
Total_Start = ml_text.find('Total\n')
Movement_Start = ml_text.find('Movement\n')
Points_Start = ml_text.find('\nPoints\n')
Value_Start = ml_text.find('\nPt/$/K\n')
DvP_Start = ml_text.find('DvP\n')
DvPRAnk_Start = ml_text.find('DvPRank\n')
PMIN_Start = ml_text.find('PMIN\n')
for pIndex in range(len(PlayerList)):
    temp = ml_text[(pIndex*4)+Team_Start+6:((pIndex+1)*4)+Team_Start+5]
    TeamList.append(temp)
   

#carriage returns between Name_Start and Salary_Start should be number of players + 1 
locSalary = [pos for pos, char in enumerate(ml_text[1+Salary_Start:]) if char == '\n']
for pIndex in range(len(PlayerList)):
    temp = ml_text[Salary_Start+locSalary[pIndex]+2:1+Salary_Start+locSalary[pIndex+1]]
    SalaryList.append(float(temp[:-1][1:])*1000)

locPosition = [pos for pos, char in enumerate(ml_text[1+Position_Start:]) if char == '\n']
for pIndex in range(len(PlayerList)):
    temp = ml_text[Position_Start+locPosition[pIndex]+2:1+Position_Start+locPosition[pIndex+1]]
    PositionList.append(temp)

locOpp = [pos for pos, char in enumerate(ml_text[1+Opp_Start:]) if char == '\n']
for pIndex in range(len(PlayerList)):
    temp = ml_text[Opp_Start+locOpp[pIndex]+2:1+Opp_Start+locOpp[pIndex+1]]
    OppList.append(temp)


locTotal = [pos for pos, char in enumerate(ml_text[1+Total_Start:]) if char == '\n' or char == '|']
for pIndex in range(len(PlayerList)):
    temp = ml_text[Total_Start+locTotal[pIndex]+2:1+Total_Start+locTotal[pIndex+1]]
    TotalList.append(temp)

locPoints = [pos for pos, char in enumerate(ml_text[1+Points_Start:]) if char == '\n']
for pIndex in range(len(PlayerList)):
    temp = ml_text[Points_Start+locPoints[pIndex]+2:1+Points_Start+locPoints[pIndex+1]]
    PointsList.append(temp)

locValue = [pos for pos, char in enumerate(ml_text[1+Value_Start:]) if char == '\n']
locValue.append(100000)
for pIndex in range(len(PlayerList)):
    temp = ml_text[Value_Start+locValue[pIndex]+2:1+Value_Start+locValue[pIndex+1]]
    ValueList.append(temp)


locDvP = [pos for pos, char in enumerate(ml_text[1+DvP_Start:]) if char == '\n' or char == '|']
for pIndex in range(len(PlayerList)):
    temp = ml_text[DvP_Start+locDvP[pIndex]+2:1+DvP_Start+locDvP[pIndex+1]]
    DvPList.append(temp)

locDvPRank = [pos for pos, char in enumerate(ml_text[1+DvPRAnk_Start:]) if char == '\n']
for pIndex in range(len(PlayerList)):
    temp = ml_text[DvPRAnk_Start+locDvPRank[pIndex]+2:1+DvPRAnk_Start+locDvPRank[pIndex+1]]
    DvPRankList.append(temp)

PMINValue = [pos for pos, char in enumerate(ml_text[1+PMIN_Start:]) if char == '\n']
PMINValue.append(100000)
for pIndex in range(len(PlayerList)):
    temp = ml_text[PMIN_Start+PMINValue[pIndex]+2:1+PMIN_Start+PMINValue[pIndex+1]]
    PMINList.append(temp)

df = pd.DataFrame(
    {'Player': PlayerList,
     'Salary': SalaryList,
     'Team': TeamList,
     'Position': PositionList,
     'Opponent': OppList,
     'Total': TotalList,
     'DvP' : DvPList,
     'DvPRank' : DvPRankList,
     'PMIN' : PMINList,
     'RG_Projection': PointsList,
     'RG_Value': ValueList
    })

df.to_csv(r'C:\Users\admin\Documents\Investments\SportsBook\roto_projections_nba.csv')

#%%
url_string = 'http://www.dailyfantasyfuel.com/nba/projections/draftkings'
browser.get(url_string)
final = pd.DataFrame()
PlayerList = []
DvPRank5List = []
VegasTotalList = []
#OpponentList = []
#DvPList = []
#LineList = []
#PowerPlayList = []
ProjectionList = []
SalaryList = []
#StartingList = []
ValueList = []

for players in range(350):
    #print(teams*2+1)
    flag1 = 1
    Player = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[1]/div[2]/div/div[1]'
    #Position = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[1]/div[3]'   
    #Team = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[1]/div[5]/span/img'
    #Opponent = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[1]/div[6]/span'
    DvPRank5 = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[3]/div[3]'
    VegasTotal = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[3]/div[1]'
    Projection = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[3]/div[5]/div[1]'
    Salary = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[3]/div[2]'
   
    try:
        ml_info = browser.find_element_by_xpath(Player)
    except NoSuchElementException:
        flag1 = 0

    if (flag1 == 1):
        ml_info = browser.find_element_by_xpath(Player)
        player_text = ml_info.get_attribute('textContent')
        player_text = player_text.strip()
        if (player_text[-2] == ' '):
            player_text = player_text[:-2]
        PlayerList.append(player_text)
    
        ml_info = browser.find_element_by_xpath(VegasTotal)
        total_text = ml_info.get_attribute('textContent')
        VegasTotalList.append(total_text)

        ml_info = browser.find_element_by_xpath(DvPRank5)
        dvp_text = ml_info.get_attribute('textContent')
        DvPRank5List.append(dvp_text) #assuming all sources end with 3 letter team code and .svgz

        ml_info = browser.find_element_by_xpath(Projection)
        proj_text = ml_info.get_attribute('textContent')
        ProjectionList.append(proj_text)
    
        ml_info = browser.find_element_by_xpath(Salary)
        salary_text = ml_info.get_attribute('textContent')
        SalaryList.append(float(salary_text[:-1][1:])*1000)
        ValueList.append(float(proj_text)/float(salary_text[:-1][1:]))    
        
    else:
        break
        

#%%

ind = pd.DataFrame({'Fuel':PlayerList})
ind['VegasTotal'] = VegasTotalList
ind['DvP_5'] = DvPRank5List
ind['Fuel_Projection'] = ProjectionList
#ind['Salary'] = SalaryList
ind['Fuel_Value'] = ValueList

nicknames = pd.read_csv(r'C:\Users\admin\Documents\Investments\SportsBook\nba name matching.csv')

#merge totals with projections
final1 = pd.merge(ind, nicknames, how='outer', on = 'Fuel')

final = pd.merge(final1,df,how='outer', left_on='RG', right_on='Player')

final.to_csv(r'C:\Users\admin\Documents\Investments\SportsBook\roto_projections_nba.csv')
#%%

#%%
#url_string = 'http://www.dailyfantasyfuel.com/nhl/odds/'
#browser.get(url_string)

"""
ids = browser.find_elements_by_xpath("//*[@id]")
for ii in ids:
    print(ii.get_attribute('id'))
"""


matches = ['2','5']  
final = pd.DataFrame()
Team1List = []
Team2List = []
Total1List = []
Total2List = []
WinPct1List = []
WinPct2List = []

for match in matches:
    url_string = 'http://www.vegasinsider.com/nhl/scoreboard/'
    browser.get(url_string)


    for teams in range(15):
        #print(teams*2+1)

        Team1 = '/html/body/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(teams+1) + ']/td[' + match + ']/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[2]/a'
        Team2 = '/html/body/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(teams+1) + ']/td[' + match + ']/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[5]/td[2]/a'

        tot = '/html/body/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(teams+1) + ']/td[' + match + ']/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[4]'

        t2 = '/html/body/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(teams+1) + ']/td[' + match + ']/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[5]/td[3]'
        t1 = '/html/body/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(teams+1) + ']/td[' + match + ']/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[3]'
  
        flag1 = 1

        try:
            ml_info = browser.find_element_by_xpath(Team1)
        except NoSuchElementException:
            flag1 = 0

        if (flag1 == 1):
            ml_info = browser.find_element_by_xpath(Team1)
            ml1_text = ml_info.text.strip()
        
            ml_info = browser.find_element_by_xpath(Team2)
            ml2_text = ml_info.text.strip()
            
            t1_info = browser.find_element_by_xpath(t1)
            t2_info = browser.find_element_by_xpath(t2) 
            tot_info = browser.find_element_by_xpath(tot) 

            
            if ((t1_info.text.strip()!='') * (t2_info.text.strip()!='') * (tot_info.text.strip()!='')):
                Team1List.append(ml1_text)
                Team2List.append(ml2_text)
                if (float(t1_info.text.strip()) < float(t2_info.text.strip())):
                    WinPct1 = -1*float(t1_info.text.strip())/(100 - float(t1_info.text.strip()))
                    if float(t2_info.text.strip()) < 0:
                        WinPct2 = -1*float(t2_info.text.strip())/(100 - float(t2_info.text.strip()))
                        WinPct1 = WinPct1 / (WinPct1 + WinPct2) 
                    else:
                        WinPct2 = 1- WinPct1
                    Ratio = (WinPct1 / (1 - WinPct1))**0.552
                    Total1 = float(tot_info.text.strip()) * Ratio/(Ratio+1)
                    Total2 = float(tot_info.text.strip()) - Total1
                else:
                    WinPct2 = -1*float(t2_info.text.strip())/(100 - float(t2_info.text.strip()))
                    if float(t1_info.text.strip()) < 0:
                        WinPct1 = -1*float(t1_info.text.strip())/(100 - float(t1_info.text.strip()))
                        WinPct2 = WinPct2 / (WinPct1 + WinPct2) 
                    else:
                        WinPct1 = 1- WinPct2
                    Ratio = (WinPct2 / (1 - WinPct2))**0.552
                    Total2 = float(tot_info.text.strip()) * Ratio/(Ratio+1)
                    Total1 = float(tot_info.text.strip()) - Total2

                Total1List.append(round(Total1,3))
                Total2List.append(round(Total2,3))
                WinPct1List.append(WinPct1)
                WinPct2List.append(WinPct2)

df = pd.DataFrame({'Nickname':Team1List})
df['Total'] = Total1List
df['WinPct'] = WinPct1List
df['OpptTotal'] = Total2List
df2 = pd.DataFrame({'Nickname':Team2List})
df2['Total']  = Total2List
df2['WinPct']  = WinPct2List
df2['OpptTotal'] = Total1List
df = df.append(df2)
#print(Team1List)
#print(Team2List)
#print(Total1List)
#print(Total2List)

df.to_csv(r'C:\Users\admin\Documents\Investments\SportsBook\NHL_totals.csv')

#%%
url_string = 'http://www.dailyfantasyfuel.com/nhl/projections/draftkings'
browser.get(url_string)
#ml_info = browser.find_element_by_xpath('//*[contains(@id, "projections")]')
#ml_text = ml_info.text.strip()

final = pd.DataFrame()
PlayerList = []
PositionList = []
TeamList = []
OpponentList = []
DvPList = []
LineList = []
PowerPlayList = []
ProjectionList = []
SalaryList = []
StartingList = []
ValueList = []

for players in range(750):
    #print(teams*2+1)
    flag1 = 1
    Player = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[1]/div[2]/div/div[1]'
    Position = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[1]/div[3]'   
    Team = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[1]/div[5]/span/img'
    Opponent = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[1]/div[6]/span'
    DvP = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[3]/div[2]'
    Line = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[3]/div[4]'
    PowerPlay = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[3]/div[3]'
    Projection = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[3]/div[6]/div[1]'
    Salary = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[3]/div[1]'
    Starting = '//*[@id="projections"]/div[1]/div/div[5]/div[' + str(players+1) + ']/div/div[1]/div[2]/div/div[3]'
    
    try:
        ml_info = browser.find_element_by_xpath(Player)
    except NoSuchElementException:
        flag1 = 0

    if (flag1 == 1):
        ml_info = browser.find_element_by_xpath(Player)
        ml1_text = ml_info.get_attribute('textContent')
        PlayerList.append(ml1_text.replace(" ", "_"))
    
        ml_info = browser.find_element_by_xpath(Position)
        ml2_text = ml_info.get_attribute('textContent')
        PositionList.append(ml2_text)

        ml_info = browser.find_element_by_xpath(Team)
        ml1_text = ml_info.get_attribute('src')
        TeamList.append(ml1_text[-8:][:-5]) #assuming all sources end with 3 letter team code and .svgz
    
        ml_info = browser.find_element_by_xpath(Opponent)
        ml2_text = ml_info.get_attribute('textContent')
        OpponentList.append(ml2_text)

        ml_info = browser.find_element_by_xpath(DvP)
        ml1_text = ml_info.get_attribute('textContent')
        DvPList.append(ml1_text)
    
        ml_info = browser.find_element_by_xpath(Line)
        ml2_text = ml_info.get_attribute('textContent')
        if not ml2_text:
            LineList.append("_")
        else:
            LineList.append(ml2_text)

        ml_info = browser.find_element_by_xpath(PowerPlay)
        ml2_text = ml_info.get_attribute('textContent')
        if not ml2_text:
            PowerPlayList.append("_")
        else:
            PowerPlayList.append(ml2_text)

        ml_info = browser.find_element_by_xpath(Projection)
        ml1_text = ml_info.get_attribute('textContent')
        ProjectionList.append(ml1_text)
    
        ml_info = browser.find_element_by_xpath(Salary)
        ml2_text = ml_info.get_attribute('textContent')
        SalaryList.append(float(ml2_text[-4:][:-1])*1000)
        ValueList.append(float(ml1_text)/float(ml2_text[-4:][:-1]))    
        
        ml_info = browser.find_element_by_xpath(Starting)
        ml2_text = ml_info.get_attribute('textContent')
        if not ml2_text:
            StartingList.append("_")
        else:
            StartingList.append(ml2_text)
    else:
        break
        



ind = pd.DataFrame({'Player':PlayerList})
ind['Position'] = PositionList
ind['Confirmed'] = StartingList
ind['Team'] = TeamList
ind['Oppt'] = OpponentList
ind['DvP'] = DvPList
ind['Line'] = LineList
ind['PowerPlay'] = PowerPlayList
ind['Projection'] = ProjectionList
ind['Salary'] = SalaryList
ind['Value'] = ValueList

#%%
#merge totals with projections
final1 = pd.merge(ind, nicknames, on='Team')

final = pd.merge(final1,df,on='Nickname')

final.to_csv(r'C:\Users\admin\Documents\Investments\SportsBook\NHL_projections.csv')

import base64
from github import Github
from github import InputGitTreeElement

user = "johnny"
password = ""
g = Github(user,password)
repo = g.get_user().get_repo('alarm-hoops')
#separate files with commas
file_list = [
    r'C:\\Users\admin\Documents\Investments\SportsBook\roto_projections_nba.csv',
    r'C:\Users\admin\Documents\Investments\SportsBook\NHL_projections.csv',
    r'C:\Users\admin\Documents\Investments\SportsBook\NHL_totals.csv'
]

file_names = [
    'roto_projections_nba.csv',
    'NHL_projections.csv',
    'NHL_totals.csv'
]
commit_message = 'python update 2'
master_ref = repo.get_git_ref('heads/master')
master_sha = master_ref.object.sha
base_tree = repo.get_git_tree(master_sha)
element_list = list()
for i, entry in enumerate(file_list):
    with open(entry) as input_file:
        data = input_file.read()
    if entry.endswith('.png'):
        data = base64.b64encode(data)
    element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
    element_list.append(element)
tree = repo.create_git_tree(element_list, base_tree)
parent = repo.get_git_commit(master_sha)
commit = repo.create_git_commit(commit_message, tree, [parent])
master_ref.edit(commit.sha)
browser.close()
browser.quit()
