#!/usr/bin/env python
# -*-coding:utf-8 -*

from library.user import User
from library.server import Server
from library.readingexcel import ExcelFile
import sys

# Gestion des utlisateurs (création, suppression, modification)
def gestionUsers(listUsersExcel, listUsers, server):
    for u in listUsersExcel:
        user = User(**u)
        user.server = server
        listUserServers = user.getlistServers()
        if server.ID in listUserServers:
            if bool(user.Remove):
                if user.DistinguishedName in listUsers:
                    user.removeUser()
            else:
                if user.DistinguishedName in listUsers:
                    if not user.compare():
                        user.updateUser()
                else:
                    user.creatUser()

# Appliquer le traitement sur chaque serveur Windows Server
def gestionByServer(listServers, listUsersExcel):
    for attServer in listServers:
        print("Traitement sur le server [ %s ]" % attServer['name'])
        server = Server(**attServer)
        server.creatServer()
        err, listUsers = server.getAllUsers()
        if err:
            continue
        gestionUsers(listUsersExcel, listUsers, server)

# Programme principal
# Ouvrir le fichier Excel et récupérer les données de chaque feuille dans une liste et appeler la fonctionne gestionByServer
def main():

    if len(sys.argv) == 1:
        print("Veuillez préciser le nom de fichier Excel à traiter !!")
        sys.exit()

    excelFile = ExcelFile(sys.argv[1])
    excelFile.openFileExcel()
    listServers = excelFile.readData("server")
    listUsersExcel = excelFile.readData("user")
    gestionByServer(listServers, listUsersExcel)


if __name__ == "__main__":
    main()

