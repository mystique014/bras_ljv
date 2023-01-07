.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

.. raw:: html

    <style> .blue {color:blue} </style>

.. role:: blue

Bouger le bras robotisé
=======================



Il est possible de bouger le bras en adoptant deux différentes stratégies.

1. En agissant directement sur les différents moteurs controlant les mouvements du bras robot (voir :red:`la zone rouge` sur l'image en bas de page). Pour cela, il suffit de modifier les sliders *pivot*, *bras 1*, *bras 2*, *bras 3* ou *pince*. Les sliders représentent les valeurs des angles à transmettre au robot pour mettre en action le moteur correspondant. La définition de ces angles est visible en cliquant sur le bouton **Schéma du Robot** situé tout en haut de l'interface. Après le mouvement de chaque slider, le mouvement du robot virtuel est directement acutalisé.

2. En faisant bouger les sliders *Robot x*, *Robot y* et *Robot z* (voir :blue:`la zone bleue` sur l'image en bas de page). Ces sliders encodent la position de la pince du robot dans le repère cartésien orthonormé centré à la base du robot. Lorsque l'utilisateur décide de bouge un ou plusieurs de ces sliders, la position du robot virtuel n'est pas automatiquement actualisé. L'utilisateur voit alors bouger un point (appelé **point d'arrivée**) dans l'espace. Ce point se voit alors doté d'une certaine couleur:

- le point d'arrivée apparaît vert si le point se situe dans une zone de l'espace que le robot peut atteindre en ayant la ventouse en position verticale (sans quoi la position n'est pas considérée comme **admissible**).

- le point d'arrivée apparaît rouge dans le cas contraire.

Une fois le point d'arrivée défini, l'utilisateur peut cliquer sur le bouton **Valider la position cartésienne**. Si le point d'arrivée était **admissible**, un calcul est automatiquement effectué permettant de placer le robot virtuel au point d'arrivé avec la ventouse placée verticalement. Notez que les sliders *pivot*, *bras 1*, ... sont automatiques actualisés pour correspondre à la nouvelle position du robot.



.. image:: ../../_static/images/bras_mouvement.png
   :width: 1000px
