#!/usr/bin/env python
# -*-coding:utf-8 -*

import json

class User:

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

    # Méthode privée, transforme une chaîne de caractètres en un dictionnaire
    # Retourne un dictionnaire
    def __strToJson(self, data):
        data = data.replace('\n', ':').split(":")
        listData = []
        for n in data:
            listData.append(n.strip())
        dictData = {}
        i = 0
        while i < len(listData):
            if (len(listData[i])):
                dictData[listData[i]] = listData[i+1]
            i += 2
        return dictData

    # Compare deux dictionnaires
    # Retourne une valeur booléenne
    def compare(self):
        res = True
        userAD = self.getUser()
        for attr_name, attr_value in self.__dict__.items():
            if attr_name in userAD.__dict__:
                if self.__dict__[attr_name] != userAD.__dict__[attr_name]:
                    res = False
        return res

    # Retourne une liste contenant les identifiants des serveurs Windows Server
    def getlistServers(self):
        if ";" in self.Server_id:
            return self.Server_id.split(";")
        else:
            return [str(int(float(self.Server_id)))]

    # Créer un utlisateur dans Windows Server
    def creatUser(self):
        res = False
        script = '''New-ADUser \
                    -Name "%s" \
                    -Path "%s" \
                    -GivenName "%s" \
                    -Enabled $%s \
                    -SamAccountName "%s" \
                    -Surname "%s" \
                    -UserPrincipalName "%s" \
                    -DisplayName "%s" \
                    -accountPassword (ConvertTo-SecureString -AsPlainText "%s" -Force) \
                    -passThru''' % (
                        self.Name, self.Path, self.GivenName, self.Enabled, self.SamAccountName, self.Surname,
                        self.UserPrincipalName, self.DisplayName, self.AccountPassword)
        try:
            output, streams, had_errors = self.server.client.execute_ps(script)
            if had_errors:
                print("For", self.DistinguishedName, "\n".join([str(s) for s in streams.error]))
            elif len(output) > 0:
                print("Le compte de l'utilisateur [ %s ] a été créé" % self.DistinguishedName)
                res = True
        except:
            print("Problème de connexion au moment de la création du compte [ %s ] !!" % self.DistinguishedName)
        finally:
            return res

    # Retourne les informations d'un utilisateur de Windows Server
    def getUser(self):
        user = None
        script = '''Get-ADUser -Identity "%s"''' % self.DistinguishedName
        try:
            output, streams, had_errors = self.server.client.execute_ps(script)
            if had_errors:
                print("For", self.DistinguishedName, "\n".join([str(s) for s in streams.error]))
            elif len(output) > 0:
                user = User(**self.__strToJson(output))
        except:
            print("Problème de connexion au moment de la consultation du compte [ %s ] !!" % self.DistinguishedName)
        finally:
            return user

    # Mettre à jour les données d'un utilisateur dans Windows Server
    def updateUser(self):
        res = False
        script = '''Get-ADUser \
                    -Identity "%s" | \
                    Set-ADUser \
                    -Enabled $%s \
                    -GivenName "%s" \
                    -SamAccountName "%s" \
                    -Surname "%s" \
                    -UserPrincipalName "%s" \
                    -DisplayName "%s"''' % (
                        self.DistinguishedName, self.Enabled, self.GivenName, self.SamAccountName, self.Surname,
                        self.UserPrincipalName, self.DisplayName)
        try:
            output, streams, had_errors = self.server.client.execute_ps(script)
            if had_errors:
                print("For", self.DistinguishedName, "\n".join([str(s) for s in streams.error]))
            else:
                print("Le compe de l'utilisateur [ %s ] a été mis à jour" % self.DistinguishedName)
                res = True
        except:
            print("Problème de connexion au moment de la mise à jour du compte [ %s ] !!" % self.DistinguishedName)
        finally:
            return res

    # Supprimer un utilisateur de Windows Server
    def removeUser(self):
        res = False
        script = '''Get-ADUser -Identity:"%s" | Remove-ADUser -Confirm:$False''' % (self.DistinguishedName)
        try:
            output, streams, had_errors = self.server.client.execute_ps(script)
            if had_errors:
                print("For", self.DistinguishedName, "\n".join([str(s) for s in streams.error]))
            else:
                print("Le compte de l'utilisateur [ %s ] a été supprimé" % self.DistinguishedName)
                res = True
        except:
            print("Problème de connexion au moment de la suppression du compte [ %s ] !!" % self.DistinguishedName)
        finally:
            return res

