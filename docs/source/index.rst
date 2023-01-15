BRAS ROBOTISE COMMANDE A DISTANCE
=================================



+------------------+--------------------+---------------+----------------+------------+
|**Documentation** | **Outil interactif | **Vidéos de   | **Construction | **Maquette |
|                  | en ligne**         | présentation  | du bras**      | numérique**|
|                  |                    | du projet**   |                |            |
+==================+====================+===============+================+============+
| |image0|         | |image1|           | |image2|      | |image3|       | |Modèle    |
|                  |                    |               |                | OnShape|   |
+------------------+--------------------+---------------+----------------+------------+
|                  | `Découverte        | `Tutoriels en | `Publication   | `Modèle    |
|                  | de                 | vidéos        | Eduscol        | OnShape    |
|                  | l’outil <ht        | <https://     | <https://edus  | <https:    |
|                  | tps://quent        | www.youtube.c | col.education  | //julesver |
|                  | induchemin.        | om/channel/UC | .fr/sti/resso  | ne14120.on |
|                  | pythonanywh        | u_MwXRD5ky9tD | urces_pedagog  | shape.com/ |
|                  | ere.com>`__        | az5NYaT0w>`__ | iques/support  | documents/ |
|                  |                    |               | -pour-une-app  | fb4ba6523b |
|                  |                    |               | roche-fonctio  | e7501f6804 |
|                  |                    |               | nnelle-de-la-  | 5163/w/285 |
|                  |                    |               | robotique>`__  | 3b905bb400 |
|                  |                    |               |                | 04b2178df9 |
|                  |                    |               |                | 2/e/b93caf |
|                  |                    |               |                | 2cf3a922b8 |
|                  |                    |               |                | 7860c5e8?a |
|                  |                    |               |                | a=true>`__ |
+------------------+--------------------+---------------+----------------+------------+


.. |image0| image:: https://img.shields.io/badge/docs-latest%20release-blue.svg
   :target: https://quentinduchemin.pythonanywhere.com
.. |image1| image:: ./_static/logos/pyany.jpg
   :target: https://quentinduchemin.pythonanywhere.com
.. |image2| image:: ./_static/logos/youtube.png
   :target: https://www.youtube.com/channel/UCu_MwXRD5ky9tDaz5NYaT0w
.. |image3| image:: ./_static/logos/eduscol-logo.jpg
   :target: https://eduscol.education.fr/sti/ressources_pedagogiques/support-pour-une-approche-fonctionnelle-de-la-robotique
.. |Modèle OnShape| image:: ./_static/logos/onshape.jpg
   :target: https://julesverne14120.onshape.com/documents/fb4ba6523be7501f68045163/w/2853b905bb40004b2178df92/e/b93caf2cf3a922b87860c5e8?aa=true
   
   
Description du projet
---------------------

``bras_ljv`` est un package Python permettant de contrôler un bras robotisé à l'aide d'une interface virtuelle.

.. image:: ./_static/images/bras_onshape.png
  :width: 400

Composantes du projet
---------------------

Le projet mobilise des outils

-- De réseau informatique
    Connexion en Point d'accès ou Ethernet

-- De programmation
    Code python

-- De visualisation
    Lien virtuel / Réel

-- D'algorithmique
    Réaliser un ordonnancement de tâches

-- De construction et modélisation
    Assemblage du robot réel, Virtuel avec Onshape

-- De connectique
    Cablage du Raspberry pi, servos, interface PWM


Applications pédagogiques
-------------------------

-- Commander un bras réel à partir d'une interface virtuelle

.. image:: ./_static/images/interface.png
  :width: 400

-- Trouver un algorithme pour réaliser un déplacement d'objets

.. image:: ./_static/images/algo.png
  :width: 200

-- Gérer les obstacles


Autres Applications
-------------------

-- Ajout d'une pince à la place de la ventouse
    Augmentation de la zone de préhension (la pince n'étant plus forcément verticale ! )

-- Reconnaissance optique d'objets:
    Déplacer, Trier, Ordonner --> déplacer, trier, ordonner des objets de façon automatique selon leur famille (forme, couleur, information ...)
    A partir de photos de l'environnement du robot, ils'agirait d'exploiter des algorithmes dits de 'Computer vision' (Détection automatique d'objets, reconstruction d'espaces en 3D).
    Une fois la scène ainsi recontruite le robot peut effectuer les tâches demandées.
    
    Exemple :

        1- Localiser à partir de photos des jetons numérotés sur un plateau de jeu

        2- Le robot empile automatiquement les jetons par numéros croissants

-- Ajout d'une base motorisée :
    Reconnaissance d'objets dans un espace pour leur traitement 

Structure de la documentation
-----------------------------

.. toctree::
    :maxdepth: 3

    presentation_robot/index.rst
    presentation_interface/index.rst
    essentiel.rst
    exercices/index.rst
    perspectives/index.rst
