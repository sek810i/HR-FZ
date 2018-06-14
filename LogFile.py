# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:07:55 2018

@author: OYB6195
"""

log=[]

def addLog(l):
    log.append(l)
    
def printLog():
       for l in log:
           print(l)
def saveLog():
    f = open('log.txt', 'w')
    for l in log:
        f.write(l + '\n')
    f.close()
           