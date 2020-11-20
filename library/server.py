#!/usr/bin/env python
# -*-coding:utf-8 -*

from pypsrp.powershell import PowerShell, RunspacePool
from pypsrp.client import Client
import json

class Server:

    # Initiation de l'objet
    def __init__(self, **attributes):
        for attr_name, attr_value in attributes.items():
            setattr(self, attr_name.strip(), str(attr_value).strip())

    # Afficher l'objet avec la fonction dir
    # Retourne un objet json
    def __repr__(self):
        return json.dumps(self.__dict__)

    # Afficher l'objet avec la fonction print
    # Retourne un objet json
    def __str__(self):
        return json.dumps(self.__dict__)

    # Transforme une chaîne de caractères en une liste
    # Retourne une liste
    def __strToList(self, data):
        data = data.split("\n")
        listData = []
        for i in range(len(data)):
            if i > 2 and data[i].strip() != '':
                listData.append(data[i].strip())
        return listData

    # Créer une connexion entre la machine Linux et un serveur Windows Server en utilisant le module pypsrp
    def creatServer(self):
        self.client = None
        try:
            self.client = Client(self.name, username=self.username, password=self.password, ssl=False)
        except:
            print("Problème de connexion au server [ %s ] !!" % self.name)

    # Retourne une liste contenant les DistinguishedName existants dans un serveur Windows Server
    def getAllPaths(self):
        paths =[]
        err = False
        script = "Get-ADOrganizationalUnit -Filter 'Name -notlike \"Domain Controllers\"' | Format-Table DistinguishedName -A"
        try:
            output, streams, had_errors = self.client.execute_ps(script)
            if had_errors:
                print("For", path, "\n".join([str(s) for s in streams.error]))
            elif len(output) > 0:
                paths = self.__strToList(output)
        except:
            err = True
            print("Problème de connexion au moment de la consultation des comptes utilisateurs !!")
        return err, paths

    # Retourne une liste contenant l'ensemble des utilisateurs existants dans une machine Windows Server
    def getAllUsers(self):
        listUsers =[]
        err = False
        errpath, paths = self.getAllPaths()
        if errpath:
            err = True
            return err, listUsers
        for path in paths:
            script = "Get-ADUser -Filter * -SearchBase '%s' | Format-Table DistinguishedName -A" % path
            try:
                output, streams, had_errors = self.client.execute_ps(script)
                if had_errors:
                    print("For", path, "\n".join([str(s) for s in streams.error]))
                elif len(output) > 0:
                    listUsers = self.__strToList(output)
            except:
                err = True
                print("Problème de connexion au moment de la consultation des comptes utilisateurs !!")
                break
        return err, listUsers
