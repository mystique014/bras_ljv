Résoudre un exercice et jouer un scénario
=========================================

Il est possible de charger un exercice préalablement défini via le menu déroulant situé dans le coin supérieur droit de l'interface. En chargeant un exercice, l'utilisateur voit apparaître un environnement pour le robot, i.e. des pièces (cylindres ou rectangles) préalablement définies et qui sont associées à des positions d'arrivée. L'objectif est alors d'utiliser le robot pour emmener chaque pièce à la position d'arrivée qui lui est associée. Cette tâche peut s'avérer plus ou moins complexe suivant les aides auxquelles le créateur de l'exercice à autoriser l'accès. Voir l':doc:`../enseignant/index` pour plus de détails.

Quand l'utilisateur pense avoir résolu l'exercice et qu'il a donc sauvegardé les différents étapes des mouvements du bras permettant cette résolution (voir la section :doc:`./bras_mouvement`), il peut appuyer sur le bouton **Film parcours**. La séquence de mouvements du robot sauvegardée va alors être jouée. Celle-ci va permettre de faire bouger les pièces présentes si les mouvements du robot programmés le permettent. L'interface permet à l'utilisateur de vérifier la faisabilité du scénario joué. En effet, un message d'erreur sera affiché si

1. deux pièces se percutent lors du scénario,

2. une pièce est lachée alors que la ventouse n'est pas en position verticale (la pièce n'est donc pas lachée correctement).


La figure ci-dessous montre les différentes étapes d'un scénario permettant d'emmener la pièce d'un exercice (en bleu) à sa position finale (en jaune). Le cone noir présent sur la portion finale du bras robot indique que la pompe de la ventouse est activée.

.. image:: ../../_static/images/steps_exo.png
   :width: 1000px
