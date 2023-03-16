L'essentiel pour commencer
==========================

Dans ce chapitre vous allez trouver toutes les informations concernant le montage, le cablage et la configuration du robot.

Le matériel :
-------------

Le bras robot ARM-21N2

.. |bras| image:: ../_static/images/bras_onshape.png
   :width: 50pt
   :height: 50pt
   :align: middle

.. |rpi| image:: ../_static/images/rpi.png
   :width: 50pt
   :height: 50pt
   :align: middle

.. |pca| image:: ../_static/images/pca9685.png
   :width: 50pt
   :height: 50pt
   :align: middle

.. |pompe| image:: ../_static/images/kit_pompe.png
   :width: 50pt
   :height: 50pt
   :align: middle

.. |alim| image:: ../_static/images/alim.png
   :width: 50pt
   :height: 50pt
   :align: middle

.. |convertisseur| image:: ../_static/images/convertisseur.png
   :width: 50pt
   :height: 50pt
   :align: middle

.. list-table:: Nomenclature
   :widths: 30 40 20 50
   :align: center
   :header-rows: 1

   * - Nom
     - Image
     - Quantité
     - Description
   * - Bras ARM-21N2
     - |bras|
     - 1
     - bras ARM-21N2
   * - Raspberry pi
     - |rpi|
     - 1
     - Modèle Rpi 3 B+
   * - Module PWM
     - |pca|
     - 1
     - PCA 9685
   * - Kit Pompe 5v
     - |pompe|
     - 1
     - Pompe 5v
        tube silicone
        ventouse
        électrovanne
        interrupteur électronique pwm
   * - Alimentation 220v AC - 12V DC
     - |alim|
     - 1
     - Alimentation 220V - 12V 10A
   * - Réducteur 12V -5V
     - |convertisseur|
     - 1
     - Régulateur Réducteur 12v - 5v  DC

Le montage du robot :
---------------------

Le modèle 3D et les plans du bras ARM-21N2 sont accessibles en cliquant sur l'image.

.. image:: ../_static/images/plan.png
  :width: 200
  :target: https://julesverne14120.onshape.com/documents/fb4ba6523be7501f68045163/w/2853b905bb40004b2178df92/e/b93caf2cf3a922b87860c5e8?configuration=List_h16Eqq6S286hiw%3DCopie_de_mise_en_plan&renderMode=0&uiState=63af27d3eb663a699c38a184

La carte SD et l'image du Rpi
-----------------------------

Pour utiliser le robot, il sera nécessaire de copier l'image du RPI sur la carte SD ou de créer sa propre carte SD en suivant ce 

.. toctree::
    :maxdepth: 1

    ./tuto.rst

Le raspberry pi est configuré au niveau wifi et le package python est déjà dans l'image.

Utilsez une carte micro SD de 16Go montée dans un adaptateur SD

1- Télécharger l'image sur le site Eduscol

2- Copier l'image sur la carte SD :

`Télécharger Win32diskImager <http://sourceforge.net/projects/win32diskimager/files/latest/download>`_

Lancer Win32diskImager

Ouvrir le fichier .img

Selectionner la carte SD (Attention au choix du bon lecteur)

Appuyez sur Write

Le cablage du module PCA9685
----------------------------

Le Raspberry Pi possède des broches réservées pour la communication I2C (GPIO2/GPIO3).
Le module est muni d’un bus I2C et d’une entrée de puissance. 
Le bus I2C est branché comme ceci:

Broche GPIO3 ou SCL à la broche SCL du module

Broche GPIO2 ou SDA à la broche SDA du module

Broche 5V à la broche Vcc du module

Broche GND à la broche GND du module

.. image:: ../_static/images/cablage.png
  :width: 400


Le montage du boitier contenant l'électronique
----------------------------------------------
Imprimer le boitier à partir des fichiers STL

`Récupérer les fichiers sur ONSHAPE <https://youtu.be/_217MOG0m8g>`__

Fixer le boitier imprimé en 3D sur le support.

.. image:: ../_static/images/composants.jpg
  :width: 400

Effectuer les branchements.

.. image:: ../_static/images/composants1.jpg
  :width: 400

Monter le RPI dans le boitier en le calant bien sur les nervures prévues pour cela.
Vérifier l'alignement de la prise RJ45

.. image:: ../_static/images/composants2.jpg
  :width: 400

Brancher l'alimentation 5V et visser le PCA99685

.. image:: ../_static/images/composants3.jpg
  :width: 400

Raccorder les servos moteurs

.. image:: ../_static/images/composants5.png
  :width: 400

port 0 : pivot

port 1 : bras1

port 2 : bras1 bis

port 3 : bras2

port 4 : bras3

port 5 : pince

port 6 : pompe

port 7 : électrovanne

Monter le capot de protection

.. image:: ../_static/images/composants4.jpg
  :width: 400

Brancher le RPI

La configuration réseau
-----------------------

L'accès au RPI se fait en wifi en se connectant au point d'accès :

SSID: raspi-webgui

Password: ChangeMe

.. image:: ../_static/images/pa.png
  :width: 400

Il n'y a rien d'autre à configurer.

Lorsque le RPI est branché, le système est entièrement fonctionnel en patientant environ 2 mn.

Dans un navigateur saisir l'adresse 10.3.141.1:8050

Vous pouvez utiliser n'importe quel média (mobile, tablette ou PC) pourvu qu'il soit connecté au point d'accès mentionné ci-dessus.

L'interface est maintenant accessible !

 .. toctree::
     :maxdepth: 1

     tuto.rst