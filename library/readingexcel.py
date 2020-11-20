#!/usr/bin/env python
# -*-coding:utf-8 -*

import xlrd
import numpy as np
import sys
from os import path
import json

class ExcelFile:

    # Initiation de l'objet
    def __init__(self, fileName):
        self.fileName = fileName

    # Afficher l'objet avec la fonction dir
    # Retourne un objet json
    def __repr__(self):
        return json.dumps(self.__dict__)

    # Afficher l'objet avec la fonction print
    # Retourne un objet json
    def __str__(self):
        return json.dumps(self.__dict__)

    # Méthode privée, permet de vérifier le paramètre d'entrée qui est un fichier fichier Excel
    # Retourne une valeur booléenne
    def __existFile(self):
        res = False
        if not path.exists(self.fileName):
            print("Le fchier [ %s ] n'existe pas !!" % self.fileName)
            sys.exit()
        elif not path.isfile(self.fileName):
            print("Le paramètre fourni [ %s ] n'est pas un fichier !!" % self.fileName)
            sys.exit()
        else:
            res = True
        return res

    # Permet d'ouvrir le fichier Excel en utilisant le module xlrd
    # Retourne une liste contenant les noms des feuilles du fichier Excel
    def openFileExcel(self):
        self.sheetNameList = []
        if (self.__existFile()):
            try:
                self.workbook = xlrd.open_workbook(self.fileName)
                self.sheetNameList = self.workbook.sheet_names()
            except xlrd.biffh.XLRDError as err:
                print("File error: {0}".format(err))
                sys.exit()
        return self.sheetNameList

    # Permet de lire une feuille du fichier Excel en utilisant le module xlrd
    # Retourne les données sous forme d'un objet
    def __openSheet(self, sheetName):
        data = None
        try:
            data = self.workbook.sheet_by_name(sheetName)
        except xlrd.biffh.XLRDError as err:
            print("Sheet error: {0}".format(err))
            sys.exit()
        return data

    # Permet de lire une feuille du fichier Excel
    # Retourne les données dans une liste où chaque élément est un dictionnaire représentant une ligne de la feuille
    def readData(self, sheetName):
        listLines = []
        if sheetName not in self.sheetNameList:
            print("The sheet name [ %s ] isn't exist !!" % sheetName)
            sys.exit()
        data = self.__openSheet(sheetName)
        numRows = data.nrows
        numCells = data.ncols
        if (numRows == 0):
            print("The sheet [ %s ] is empty" % sheetName)
        for i in range(numRows):
            line = dict()
            if i > 0:
                path = ""
                displayName = ""
                for j in range(numCells):
                    colName = data.cell_value(0, j)
                    colValue = str(data.cell_value(i, j))
                    if colName == "ID":
                        colValue = int(float(colValue))
                    # if j > 0:
                    if colName in ["OU", "DC"] and colValue != "":
                        path = path + colName + "=" + colValue + ","
                    else:
                        line[colName] = colValue
                    if colName in ["DisplayName"]:
                        displayName = colValue
                        line[colName] = colValue
                line["Path"] = path[:-1]
                line["DistinguishedName"] = "CN=" + displayName + "," + path[:-1]
                listLines.append(line)
        return listLines
