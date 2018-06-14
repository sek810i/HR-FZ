# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 15:34:33 2018

@author: OYB6195
"""

import xlrd
import LogFile as lf

def printList(ls):
    for item in ls:
        print(item)

def isDouble(ls):
    elem=[]
    double = []
    for item in ls:
        if not item[1] in elem:
            elem.append(item[1])
        else:
            double.append(item)
    return False if len(double)==0 else double

def notNull(s):
    if str(s) == '' or len(str(s))==0 or s==0 or str(s) == 'ID':
        return False
    else:
        return True
def isRestName(s):
    if str(s).lower() != 'AC'.strip().lower() and str(s).strip().lower() != 'Ресторан'.lower() and str(s).strip().lower() != 'Итого'.lower() and str(s).strip()!='':
        return(True)
    else:
        return(False)
    
def pprCheck(filePath):
    workbook = xlrd.open_workbook(filePath)
    worksheet = workbook.sheet_by_name(u'Структура рынка')
    
    row=0
    rowsID = []
    
    while True:
        try:
            code = worksheet.cell(row,1).value
            name = worksheet.cell(row,2).value
            if notNull(code) or (not notNull(code) and 'KFC'.lower() in str(name).lower()):
                rowsID.append([row,str(code).strip(),str(name).strip()])
            row+=1
        except IndexError:
            break
    #printList(rowsID)    
    Double = isDouble(rowsID)
    if Double != False:
        lf.addLog(filePath+'Дубли кодов('+str(Double)+')') 
        #printList(isDouble(rowsID)) #del
    nullCode = [item for item in rowsID if not notNull(item[1])]
    if nullCode:
        lf.addLog(filePath+'Пустой код('+str(nullCode)+')') 
        #printList(nullCode) #del
    
def turnoverCheck(filePath):
    workbook = xlrd.open_workbook(filePath)
    worksheet = workbook.sheet_by_index(0)
    
    row=0
    rowsID = []
    
    while worksheet.cell(row,0).value != 'ID':
        row+=1
    
    while True:
        try:
            code = worksheet.cell(row,0).value
            name = worksheet.cell(row,1).value
            if notNull(code) or (not notNull(code) and isRestName(name)):
                rowsID.append([row,str(code).strip(),str(name).strip()])
            row+=1
        except IndexError:
            break
    
    #printList(rowsID)
    #print('Дубли:')
    Double = isDouble(rowsID)
    if Double != False:
        lf.addLog(filePath+'Дубли кодов('+str(Double)+')') 
        #printList(isDouble(rowsID)) #del
    #print('Пустые номера:')
    nullCode = [item for item in rowsID if not notNull(item[1])]
    if nullCode:
        lf.addLog(filePath+'Пустой код('+str(nullCode)+')') 
        #printList(nullCode) #del