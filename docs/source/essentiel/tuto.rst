Tutoriel
========

Copyright (C) 2023 Stéphane Duchemin
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/

Les étapes de création de la carte SD

**1 - Télécharger et installer l'image de raspbian à partir de https://www.raspberrypi.com/software/**

Choisir "imager" version Raspbian 64bits lite dans Raspberry pi OS (other)

Pour le stockage --> Choisir votre carte SD (ATTENTION à bien sélectionner votre carte SD !)

Cliquer sur la roue crantée 

    Activer SSH

    Nom utilisateur : pi

    Mot de passe: pi

    Configurer le WIFI

        Saisir le SSID

        Saisir le mot de passe

    Pays WIFI : fr 

    Définir les réglges locaux

        Fuseau horaire : EUROPE:PARIS

        Type de clavier : fr 

**2 - Monter la carte SD sur le RPI**

récupérer l'adresse ip du RPI grace à l'outil "Advanced_IP_Scanner"

**3 - Se connecter en ssh sur le RPI sur la même plage réseau en 192.168.1.....**

ouvrir une fenêtre bash et taper ssh pi@192.168.1...

saisir le mdp du compte pi

**4 - Installer le point d'accès RASPAP** 

sur le github RASAP suivre la procédure d'installation

https://github.com/RaspAP/raspap-webgui

accès interface raspap :

10.3.141.1

    username : admin

    pwd : secret

WIFI :

    SSID  : raspi-webgui

    Password : ChangeMe

reboot

**5 - Copier le projet bras-ljv dans le /home/pi/bras**

https://github.com/mystique014/bras_ljv

**6 - Installer les paquets python en ligne de commande**

ATTENTION SE CONNECTER en SSH puis sudo su (faire les install de paquet en super user)

Pip3 install dash, scipy, pulp, etc....

Penser à installer le paquet pour le module PCA9685 adafruit

sudo pip3 install adafruit-circuitpython-pca9685

**7 - Créer un fichier bash lance.sh contenant**

cd /home/pi/bras

python3 app.py

**8 - Créer une tache cron pour lancer le fichier lance.sh au reboot du RPI** 

créer un dossier logs dans /home/pi

en sudo su 

crontab -e et ajouter à la fin du fichier

@reboot sh /home/pi/lance.sh > /home/pi/logs/log.txt 2>&1

reboot

That's all !