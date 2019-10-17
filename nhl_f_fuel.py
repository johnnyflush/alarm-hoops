# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 08:08:40 2018

@author: e303797
"""




###################################################
# Load Packages: 
###################################################
# Controlling the Browser - Webscrape for Websites with logins
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Reading Excel Spreadsheets
import openpyxl
import os

# Error Reading
import sys

# DataFrames
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

salary_df = list()
skater_df = list()
goals_df = list()
assists_df = list()
shots_df = list()
blocks_df = list()
ppp_df = list()
toi_df = list()
team_df = list()
line_df = list()
ppline1_df = list()
ppline2_df = list()


capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"


# Opens Chrome & goes to the Website (Must download chrome driver from the interwebs)
chrome_driver_path = r'C:\Users\e303797\Downloads\chromedriver.exe' #path of the driver you installed
browser = webdriver.Chrome(chrome_driver_path, desired_capabilities=capa)
wait = WebDriverWait(browser, 90)



browser.get('http://www.dailyfantasyfuel.com/nhl/projections/')
'''
first = '//*[@id="projections"]/div/table/tbody/tr[1]/td[2]/div[1]/span[1]'
last = '//*[@id="projections"]/div/table/tbody/tr[1]/td[2]/div[1]/span[2]'
salary = '//*[@id="projections"]/div/table/tbody/tr[1]/td[3]'
position = '//*[@id="projections"]/div/table/tbody/tr[1]/td[4]'
team = '//*[@id="projections"]/div/table/tbody/tr[1]/td[6]/span'
opponent = '//*[@id="projections"]/div/table/tbody/tr[1]/td[7]/span'
pp = '//*[@id="projections"]/div/table/tbody/tr[1]/td[12]'
line = '//*[@id="projections"]/div/table/tbody/tr[1]/td[13]'
points = '//*[@id="projections"]/div/table/tbody/tr[1]/td[17]/div[1]'
'''
#%%
First_Name = []
Last_Name = []
Salary = []
Position = []
Team = []
Oppt = []
PP = []
Line = []
Points = []
Proj_Total = []

row = 1
last = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[2]/div[1]/span[2]'
try:
    browser.find_element_by_xpath(last)
    run_script = True
except NoSuchElementException:
    row = 0

while row > 0:
    xp = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[2]/div[1]/span[1]'
    tmp = browser.find_element_by_xpath(xp)
    First_Name.append(tmp.text.strip())
    xp = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[2]/div[1]/span[2]'
    tmp = browser.find_element_by_xpath(xp)
    Last_Name.append(tmp.text.strip())
    xp = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[3]'
    tmp = browser.find_element_by_xpath(xp)
    tmp = tmp.text.strip()
    Salary.append(int(float(tmp[1:][:-1])*1000))
    xp = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[4]'
    tmp = browser.find_element_by_xpath(xp)
    Position.append(tmp.text.strip())
    xp = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[6]/span'
    tmp = browser.find_element_by_xpath(xp)
    Team.append(tmp.text.strip())
    xp = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[7]/span'
    tmp = browser.find_element_by_xpath(xp)
    Oppt.append(tmp.text.strip())
    xp = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[12]'
    tmp = browser.find_element_by_xpath(xp)
    PP.append(tmp.text.strip())
    xp =  '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[13]'
    tmp = browser.find_element_by_xpath(xp)
    Line.append(tmp.text.strip())
    xp = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[10]'
    tmp = browser.find_element_by_xpath(xp)
    Proj_Total.append(tmp.text.strip())
    xp = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[17]/div[1]'
    tmp = browser.find_element_by_xpath(xp)
    Points.append(tmp.text.strip())   
    
    row += 1
    last = '//*[@id="projections"]/div/table/tbody/tr[' + str(row) + ']/td[2]/div[1]/span[2]'
    try:
        browser.find_element_by_xpath(last)
        run_script = True
    except NoSuchElementException:
        row = 0
                     
lineup = pd.DataFrame(
        {'First_Name': First_Name,
         'Last_Name': Last_Name,
         'Position': Position,
         'Salary': Salary,
         'Proj_Total': Proj_Total,
         'Line' : Line,
         'Team' : Team,
         'Oppt' : Oppt,
         'PP' : PP,
         'Points' : Points
        })
lineup['Value'] = lineup.apply(lambda row: float(row.Points) / float(row.Salary) , axis=1)  
lineup.Value = lineup.Value * 1000  
lineup = lineup.sort_values(by='Value', ascending=False)
lineup.to_csv(r'C:\Users\e303797\Documents\Trash\lineup.csv')