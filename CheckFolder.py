# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 16:54:35 2018

@author: OYB6195
"""

import os
from datetime import datetime, date, time
import CheckExcel
import LogFile as lf



def joinPath(a,b):
    return str(a) + '\\' + str(b)



def isInt(s): 
    try: 
        int(s)
        return True
    except ValueError:
        return False


def checkYear(y):
    if int(y[-1]) != int(date.today().year) or date.today().month == 1:
        lf.addLog(company + ': Нет текущего года')
    if sum(y) != int(((y[0]+y[-1])/2)*len(y)):
        lostYear=[]
        for i in range(y[0],y[-1]):
            if i not in y:
                lostYear.append(i)
        lf.addLog(company + ': Разрыв в годах (отсутствует:' + str(lostYear) + ')')

def checkMonth():
    months=[]
    lostMonths = []
    strMonths=["январь","февраль","март",
                   "апрель","май","июнь",
                   "июль","август","сентябрь",
                   "октябрь","ноябрь","декабрь"]
    if int(year) != int(date.today().year):
        for month in [c +' '+ str(year) for c in strMonths]:
            if os.path.exists(joinPath(yearPath,month)):
                months.append(month)
            else:
                lostMonths.append(month)
    else:
        for month in [c +' '+ str(year) for c in strMonths[:int(date.today().month)]]:
            if os.path.exists(joinPath(yearPath,month)):
                months.append(month)
            else:
                lostMonths.append(month)
    if len(lostMonths)>0:
        lf.addLog(company +' '+ str(year) + ': нет месяца (отсутствует:' + str(lostMonths) + ')')
    return months

        
def fr(f):
    return f[0]+'.'+f[1]
def dualfr(f,i):
    return f[0]+'.'+f[1][i]
def notfr(f):
    return f[0] + '.' + 'xls' if f[1]=='xlsx' else 'xlsx'

def checkFile(path): #временная функция без обработки самих файлов
    nameFiles=[['3 turnover','xls','turnoverCheck'],
               ['PPR MARKET','xls','pprCheck'],
               ['ОСА','xlsx'],
               ['HR statistics by company',['xlsx','xls']]]
    for file in nameFiles:
        if not type(file[1]) is list:
            if not os.path.exists(joinPath(monthPath,fr(file))):
                if os.path.exists(joinPath(monthPath,notfr(file))):
                    lf.addLog(monthPath + ' : Ошибка формата файла ('+notfr(file)+' должен быть '+fr(file)+')')
                else:
                    lf.addLog(monthPath + ' : отсутствует файл ('+fr(file)+')')
            else:
                if len(file)==3:
                    fp=joinPath(monthPath,fr(file))
                    f = getattr(CheckExcel, file[2])
                    f(fp)
        else:
            if not os.path.exists(joinPath(monthPath,dualfr(file,0))) or not os.path.exists(joinPath(monthPath,dualfr(file,1))):
                lf.addLog(monthPath + ' : отсутствует файл ('+file[0]+')')
            else:
                if len(file)==3:
                    if os.path.exists(joinPath(monthPath,dualfr(file,0))):
                        fp=joinPath(monthPath,dualfr(file,0))
                    else:
                        fp=joinPath(monthPath,dualfr(file,1))
                    f = getattr(CheckExcel, file[2])
                    f(fp)
            
def checkFileFn(path,fn):
    print(1)

root = '\\\\MOSINT02\\Integration Data\\Box Sync\\HR-отчеты (PPR+TO)'

companyFolders = os.listdir(root)

for company in companyFolders:
    print(company)
    companyPath = joinPath(root,company)
    yearFolders = os.listdir(companyPath)
    years = []
    for year in yearFolders:
        if isInt(year):
            years.append(int(year))
    checkYear(years)
    for year in years:
        yearPath = joinPath(companyPath,year) 
        monthsFolders = os.listdir(yearPath)
        months=checkMonth()
        for month in months:
            monthPath = joinPath(yearPath,month)
            checkFile(monthPath)
                        
lf.printLog()
lf.saveLog()
