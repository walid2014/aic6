# Automatisation de la gestion des comptes utilisateurs de Windows Server

Ce programme que j'ai implémenté en langage de programmation Python (vesrion 3.9.0), permet, à partir d'une machine sous Linux, la gestion des comptes utilisateurs de Windows Server définie dans un fichier Excel dont un template est fourni avec le programme.

Tout d'abord, je voudrais signaler que ce projet peut être enrichi afin de gérer l'ensemble des attributs des comptes utilisateurs de Windows Server qui sont plus d'une centaine d'attributs. De plus, il peut être élargi pour comporter l'ensemble des commandes Power Shell qu'on peut exécuter sur Windows Server.

Le programme est composé de 4 scripts, un template Excel et le fichier [README.md](README.md) que vous êtes en train de lire.

L'arborescence de l'ensemble des fichiers est la suivante :

```bash
├── library
│ ├── readingexcel.py
│ ├── server.py
│ └── user.py
├── main.py
├── README.md
└── users.xlsx
```

J'ai séparé le programme en différents scripts afin de respecter le modèle MVC (Modèle, Vue, Contrôle), à savoir que dans notre cas il n'y a pas de vue.

### [library](library)

C'est un répertoire qui contient 3 scripts python, chacun de ces scripts est une classe python.

### [readingexcel.py](library/readingexcel.py)

Ce script, qui est une classe Python, permet d'ouvrir le fichier Excel et d'exporter les données de chacune des feuilles dans une liste dont chaque élément est un dictionnaire représentant une ligne de la feuille.  
Ce script est dépendant du module [xlrd](https://pypi.org/project/xlrd/)\.

### [server.py](library/server.py)

Ce script, qui est une classe Python, permet la connexion d'une machine Linux sur les différentes machines sous Windows Server, il permet également d'exécuter des scripts et des commandes Power Shell.  
Ce script est dépendant du module [PyPSRP](https://www.bloggingforlogging.com/2018/08/14/powershell-remoting-on-python/), qui prend en charge tous les types d'authentifications tels que Basic, Certificate, Negotiate, Kerberos et CredSSP. Dans ce programme, j'ai utilisé l'authentification CredSSP, pour cela, il faut installer aussi le module CredSSP.  
Donc, tous les traitements que nous pouvons faire par des commandes Power Shell sur Windows Server nous pouvons les faire à partir d'une machine Linux en utilisant ce module.

### [user.py](library/user.py)

Ce script, qui est une classe Python, permet la gestion des comptes d'utilisateurs, création, modification, suppression avec un minimum d'attributs qui sont nécessaires pour la création de ces comptes et qui sont précisés dans le fichier Excel.  
Comme j'ai dit auparavant, cela peut être étendu sur l'ensemble des attributs et des fonctionnalités de Windows Server, vu qu'on peut tout gérer par des scripts et des commandes Power Shell.

### [users.xlsx](users.xlsx)

Ce fichier est le template Excel, la structure de ce fichier doit être respectée pour les noms des colonnes, leurs ordres, leurs types de données et enfin les noms des deux feuilles qui sont (user et server).  
Par contre, le nom du fichier peut être n'importe quel nom à condition qu'il respecte la nomination des fichiers de système d'exploitation sur lequel vous exécuter le programme.  
La feuille "user" contient l'ensemble des utilisateurs.  
La feuille "server" contient l'ensemble des serveurs "Windows Server".  
Le nom de ce fichier avec son chemin doit être accessible et en lecture seule et sera fourni comme paramètre d'entrée à la ligne de commande d'exécution du programme.

### [main.py](main.py)

Ce script qui doit être exécuté sur un terminal Linux après chaque modification dans le fichier Excel.  
Le compte rendu de l'exécution sera afficher dans le terminal.

## Prérequis

Pour le bon fonctionnement de ce programme, il faut respecter certains prérequis :

1. Ce programme a été développé et testé sur une machine virtuelle Debian 10. Pour d'autres version je vous conseille d'adapter surtout les modules Python ([xlrd](https://pypi.org/project/xlrd/), [PyPSRP](https://www.bloggingforlogging.com/2018/08/14/powershell-remoting-on-python/) en consultant leurs documentations).
2. Les machines Windows Server, sur lesquelles j'ai appliqué le programme, sont sous le système Windows Server 2016 (Version Standard) installées sur VMWare Fusion.
3. Il faut installer Python 3.9.0 sur la machine Debian 10 (Je n'ai pas testé sur d'autres version).
4. Il faut vérifier la connexion entre la machine Debian 10 et les machines Windows Server avec des ping dans les deux sens.

## Installation Python sur Debian 10

D'abord, il faut mettre à jour le système :

```bash
$ sudo apt-get update
```

Installer les paquets Linux suivants :

```bash
$ sudo apt-get install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev liblzma-dev
```

Télécharger Python (Version 3.9.0) :

```bash
$ wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz
```

Si le paquet "wget" n'est pas installé par défaut, il faut l'installer via la commande :

```bash
$ sudo apt-get install wget
```

Décompresser le fichier "Python-3.9.0.tar.xz" via la commande :

```bash
$ tar -xf Python-3.9.0.tar.xz
```

Le déplacer dans le répertoire Python-3.9.0 :

```bash
$ cd Python-3.9.0
```

Exécuter les trois commandes suivantes dans l'ordre :

```bash
$ ./configure --enable-optimizations
$ make -j 4
$ sudo make altinstall
```

Vérifier que Python 3.9.0 est bien installé via la commande :

```bash
$ python3.9 --version
Python 3.9.0
```

### Préparation de l'environnement du travail

```bash
$ mkdir ~/myapp && cd ~/myapp   # créer un répertoire et déplacer dans celui-ci
$ python3.9 -m venv env         # création de l'environnement du travail
$ source env/bin/activate       # pour activer l'environnement du travail
(env) $ python -v               # vérifier la version Python dans l'environnement du travail
(env) $ deactivate              # pour désactiver l'environnement du travail
```

Installer les paquets Linux suivants, qui sont nécessaires pour le module [PyPSRP](https://www.bloggingforlogging.com/2018/08/14/powershell-remoting-on-python/) de Python :

```bash
$ sudo apt-get install gcc python3-dev libkrb5-dev
```

Installer à partir de l'environnement de travail les deux modules pythons [xlrd](https://pypi.org/project/xlrd/) et [PyPSRP](https://www.bloggingforlogging.com/2018/08/14/powershell-remoting-on-python/) :

```bash
(env) $ pip install xlrd
(env) $ pip install pypsrp[kerberos,credssp]  # installer le module kerberos ce n'est pas obligatoire pour ce programme
```

## Utilisation du programme

D'abord, le fichier Excel doit être rempli par les informations concernant les utilisateurs à traiter et les serveurs Windows Server sur lesquels le traitement sera appliqué.

Ensuite, le programme s'exécute sur un terminal Linux par la ligne de commande suivante :

```bash
(env) $ python main.py users.xlsx
```

## Particularité du programme

Le programme dans son état actuel prend en compte les attributs qui sont dans l'entête de la feuille "user" du fichier Excel [users.xlsx](users.xlsx) à savoir :

**Name** : c'est le nom de l'utilisateur et c'est l'identifiant de l'utilisateur dans un domaine Active Directory, cette valeur une fois définie, ne peut pas être modifier, comme le montre la figure suivante :

<p align="center">
<img
  src="https://github.com/walid2014/images/blob/main/image01.png"
  width="600"
  height="450px"
/>
</p>

**GivenName** : c'est le prénom de l'utilisateur, comme le montre l'image suivante :

<p align="center">
<img
  src="https://github.com/walid2014/images/blob/main/image02.png"
  width="400"
  height="420px"
/>
</p>

**Surname** : c'est le nom de l'utilisateur, comme le montre l'image suivante :

<p align="center">
<img
  src="https://github.com/walid2014/images/blob/main/image03.png"
  width="400"
  height="420px"
/>
</p>

**SamAccountName** : c'est le nom d'ouverture de session de l'utilisateur (antérieur à Windows 2000), comme le montre l'image suivante :

<p align="center">
<img
  src="https://github.com/walid2014/images/blob/main/image04.png"
  width="400"
  height="420px"
/>
</p>

**AccountPassword** : c'est le mot de passe de l'utilisateur, ce mot de passe doit respecter les conditions définies par Windows Server.

**DisplayName** : c'est le nom complet de l'utilisateur, comme le montre l'image suivante :

<p align="center">
<img
  src="https://github.com/walid2014/images/blob/main/image05.png"
  width="400"
  height="420px"
/>
</p>

**UserPrincipalName** : c'est le nom d'ouverture de session de l'utilisateur, comme le montre l'image suivante :

<p align="center">
<img
  src="https://github.com/walid2014/images/blob/main/image06.png"
  width="400"
  height="420px"
/>
</p>

**Enabled** : prend une valeur booléenne (True ou False), la valeur par défaut est True, qui permet d'activer ou désactiver le compte utilisateur.

**CN** : le nom commun de l'utilisateur, cet attribut peut être répété plusieurs fois selon le besoin. Le programme dans sa version actuelle ne gère qu'un seul attribut.

**OU** : l'unité organisationnelle, cet attribut peut être répété plusieurs fois selon le besoin. Le programme dans sa version actuelle ne gère qu'un seul attribut. Attention, la création des unités organisationnelles ne sont pas prises en compte dans la version actuelle. Pour tester le programme avec les jeux de données, il faut créer l'unité organisationnelle "mycompany".

**DC** : les composants de domaine, cet attribut peut être répété plusieurs fois selon le besoin. Le programme dans sa version actuelle prend en charge cette répétition, comme le montre les jeux de données dans le fichier Excel.

Les trois attributs **CN, OU** et **DC**, forme ce qu'il s'appelle l'attribut "DistinguishedName" de l'Active Directory, cet attribut permet d'identifier l'utilisateur d'une manière unique dans l'annuaire.

**Remove** : cet attribut ne fait pas partie des attributs d'Active Directory, il est défini juste pour supprimer un utilisateur si sa valeur est True, et qu'il n'a aucun effet si sa valeur est vide.

**Server_id** : cet attribut ne concerne que le programme, il permet d'identifier les machines Windows Server sur lesquelles les utilisateurs doivent être créés. Les valeurs de cet attribut doivent être parmi les valeurs de l'attribut "ID" de la feuille server du fichier Excel. S'il faut créer l'utilisateur sur plusieurs Windows Server, il faut séparer les valeurs par des ";".

Si vous n'avez pas configuré un server DNS, il faut ajouter les noms de Windows Server, qui sont dans la colonne "name" de la feuille "server" du fichier Excel, dans le fichier /etc/hosts de la machine Linux.

Je voudrais juste signale aussi que l'attribut SSL dans la feuille "server" du fichier Excel a toujours la valeur "False", car il a besoin un certificat valide (ce que je ne possède pas 😢).

## L'intérêt de ce programme

Le but de ce programme est d'automatiser la gestion des utilisateurs à partir d'un fichier Excel qui facilite le travail d'un administrateur infrastructure et cloud, au moment de l'arrivée d'un flux d'utilisateurs en tant que visiteurs dans l'entreprise ou des apprentis dans un centre de formation, il est facile de leur créer des comptes utilisateurs rapidement et les supprimer ou les désactiver juste après, avec une seule ligne de commande après avoir rempli le fichier Excel par les informations des utilisateurs.
