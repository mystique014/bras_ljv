Interface Enseignant
====================


L'interface *Enseignant* permet de la création d'exercices. L'enseignant peut créer des environnements dans lesquels les élèves doivent effectuer les tâches spécifiées. 

Plus précisément, l'enseignant peut définir deux types de pièces: des cylindres ou des rectangles. Pour chaque pièce créée, l'enseignant définit non seulement une position initiale mais aussi un position d'arrivée. L'élève aura la tâche de déplacer chaque pièce de son point de départ à son point d'arrivée.


Procédure pour définir un couple (position initiale, position finale) pour une pièce de l'exercice:

1. l'enseignant commence par choisir la pièce qu'il souhaite créer (i.e. un cylindre ou un rectangle).

2. l'enseignant modifie alors les sliders pour définir:

- les caractéristiques de la pièce (i.e. le rayon et la hauteur pour le cylindre, et la hauteur, la largeur, la longueur et l'orientation dans le plan (x,y) pour le rectangle),

- la position initiale de la pièce,

- la position finale souhaitée pour la pièce.  

3. L'enseignant peut alors cliquer sur le bouton **Sauvegarde la pièce** si les paramètres de l'étape 2. lui conviennent.

4. L'enseignant peut alors créer de nouvelles pièces selon le même principe. Une fois toutes les pièces créées, l'enseignant peut cliquer sur le bouton **Sauvegarder l'exercice** et spécifier un nom de sauvegarde pour l'exercice. Lorsqu'un exercice est sauvegardé, un fichier .pkl (format pickle pour Python) est créé et sera lu pour charger l'exerce dans l':doc:`../eleve/index`. De plus, un fichier excel du même nom est aussi créé ce qui permet d'avoir facilement accès au caractéristiques de l'exercice pour l'enseignant et de potentiellement charger les caractéristiques sur d'autres plateformes (comme OnShape) pour créer les pièces 3D requises pour l'exercice. Ces deux fichiers sont enregistrés dans le dossier `exercices` situé à la racine du projet.  



Pour rendre son exercice plus ou moins difficile, l'enseignant peut octroyer (ou non) l'accès à certains outils à l'élève. En particulier, l'enseignant peut:

- autoriser (ou pas) l'élève à pouvoir visualiser l'espace des *points admissibles* dans l'exercice (voir la section :doc:`../eleve/options_affichage` pour plus de détails).

- autoriser (ou pas) les mouvements en coordonnées cartésiennes dans l'exercice. Si l'option est activée, l'élève peut positionner le robot en définissant en coordonnées cartésiennes le point d'arrivée pour la ventouse et un calcul automatique sera effectué pour positionner le bras correctement. Si cette option est désactivée, l'élève devra effectuer tous les mouvements du bras uniquement en actionnant les différents moteurs de façon directe (i.e. en modifiant les angles *pivot*, *bras 1*, *bras 2*, *bras 3* et *pince*).

- autoriser (ou pas) lecture possible des coordonnées cartésiennes sur la figure 3D.



