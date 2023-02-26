Tutoriel
========

Copyright (C) 2023 Stéphane Duchemin
# Licensed under the Creative Commons Attribution-ShareAlike License 4.0 (International) (CC-BY-SA 4.0) -https://creativecommons.org/licenses/by-sa/4.0/

Les étapes de création de la carte SD

**1 - Télécharger l'image de raspbian sur https://www.raspberrypi.com/software/**

Utiliser imager version Raspbian 64bits lite

https://downloads.raspberrypi.org/imager/imager_latest.exe

préconfigurer ssh locales nom utilisateur et mdp (pi/pi)

**2 - Décompacter et copier l'image sur carte SD 16Go**

Utiliser Win 32 Diskimager

**3 - Monter la carte SD sur le RPI**

récupérer l'adresse ip du RPI grace à l'outil "Advanced_IP_Scanner"

**4 - Se connecter en ssh sur le RPI sur la même plage réseau en 192.168.1.....**

ouvrir une fenêtre bash (gitbash) taper ssh pi@192.168.1...

saisir le mdp du compte pi

**5 - Installer le point d'accès RASPAP** 

sur le github RASAP suivre la procédure d'installation

https://www.raspberrypi.com/software/

https://downloads.raspberrypi.org/imager/imager_latest.exe

accès interface raspap :

10.3.141.1

username : admin

pwd : secret

WIFI :

SSID  : raspi-webgui

Password : ChangeMe

reboot

**6 - Installer les paquets python en ligne de commande**

ATTENTION SE CONNECTER en SSH puis sudo su (faire les install de paquet en super user)

Pip3 install dash, scipy, pulp, etc....

Penser à installer le paquet pour le module PCA9685 (adafruit....)

**7 - Copier le projet bras-ljv dans le /home/pi/bras**

**8 - Créer un fichier bash lance.sh contenant**

cd /home/pi/bras

python3 app.py

**9 - Créer une tache cron pour lancer le fichier lance.sh au reboot du RPI** 

créer un dossier logs dans /home/pi

en sudo su 

crontab -e et ajouter à la fin du fichier

@reboot sh /home/pi/lance.sh > /home/pi/logs/log.txt 2>&1

reboot

That all !
