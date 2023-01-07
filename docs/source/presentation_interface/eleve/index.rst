Interface Eleve
===============


L'interface *Elève* est le coeur du projet Bras LJV. Via cet interface, un utilisateur peut expérimenter des mouvements du robot virtuel (voir comment :doc:`./bras_mouvement`), résoudre des exercices prédéfinis (voir l':doc:`../enseignant/index`), associer tous ou certaines des mouvements commandés via l'interface au robot réel (voir les :doc:`./options_affichage`), ...


.. image:: ../../_static/images/interface.png
   :width: 1000px


Les éléments principaux actionnables ou activables sur l'interface sont les suivants:




- **Authentification** (*Bouton*): Permet de s'authentifier pour l'accès à l'interface Eleve ou à l':doc:`../enseignant/index`. Un identifiant et un mot de passe sont requis pour l'accès à la plateforme Enseignant.

- **Schéma du robot** (*Bouton*): Permet de visualiser un schéma du bras robot (et de comprendre en particulier la définition des différents angles qui caractérisent sa position).

- **Film parcours** (*Bouton*): Permet de jouer le film de toutes la séquence des mouvements du robot qui a été sauvegardée.

- **Supprimer la sauvegarde** (*Bouton*): Ce bouton permet de supprimer la séquence des positions du robot qui aura été préalablement sauvegardée.

- **Retour à la position initiale** (*Bouton*): Une position initiale a été définie par défaut pour le robot virtuel. Appuyer sur ce bouton permet d'envoyer le robot virtuel à cette position.

- **Choix d'un exercice** (*Menu déroulant*): Permet de sélectionner l'un des exercices (et les pièces qui lui sont associées). Par défaut, aucun exercice n'est chargé. Pour plus de détails, voir :doc:`./exercices`.

- **Options d'affichage** (*Cases à cocher*): L'interface permet d'activer ou pas certaines options et nous renvoyons à la section :doc:`./options_affichage` pour plus de détails.

- **Mouvements du robot** (*Sliders*): Des sliders permettent de bouger le robot (voir :doc:`./bras_mouvement`).


Nous renvoyons au sections ci-dessous pour une description plus précise des fonctionnalités de la plateforme.


.. toctree::
    :maxdepth: 1

    bras_mouvement.rst
    options_affichage.rst
    exercices.rst
