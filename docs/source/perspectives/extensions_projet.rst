Extensions du projet
====================


Le projet ainsi lancé offre un large panel de possibles extensions qui pourraient aussi bien intéresser le corps enseignant que les industriels. Ci-dessous, nous souhaitons mettre en lumière certaines perspectives qui nous sommes particulièrement pertinentes.

1. **Passer de la ventouse à une pince (ou main artificielle)**

Le bras actualisé utilisé dispose d'une ventouse. Cette caractéristique fait que le bras robot est particulièrement adapté pour prendre et déposer des pièces lorsque la portion finale du bras est verticale. Si le bras robotisé dispose d'une pince (et non pas d'une ventouse), il serait souhaitable détendre le code développé dans le projet Bras LJV afin que la zone admissible (voir :doc:`../presentation_interface/eleve/options_affichage`) pour le bras ne soit pas restreinte à la zone où la portion finale du bras soit en position verticale. Cela implique notamment détendre la fonction du projet Bras LJV qui calcule:

- la zone des points admissibles pour le robot,

- les paramètres caractérisant la position du bras robot permettant que la pince de ce dernier se trouve à une certaine position :math:`[x,y,z]` si ce point est effectivement admissible.

2. **Passer à l'automatisation complète du robot à l'aide d'une webcam embarquée**

En disposant une caméra filmant le robot et son environnement, il serait possible d'utiliser des algorithmes de **Computer Vision** (type détection d'objets), permettant de reconnaître les objets présents autour du robot (et de potentiellement lire des informations inscrites sur ces objets) afin que le robot puisse ensuite automatique réaliser une tâche donnée. Donnons un exemple concret.  Il serait possible de disposer par terre autour du robot des jetons numérotés. A partir des images de la webcam, l'algorithme de Computer Vision pourrait identifier les positions des pièces et lire les numéros inscrits sur eux. Ensuite, le robot pourrait automatiquement empiler les jetons par numéros croissants à une position marquée par une croix sur le sol. La tâche du robot pourrait être complexifiée en ajoutant des obstacles dans son environnement.

**Mots clés du projet:** Traitement d'image, Computer stereo vision.

3. **Permettre au bras robot de se déplacer dans l'espace: Optimiser la gestin d'un entrepôt**

Il pourrait être permis au robot d'être positionné sur une plateforme mobile dans l'espace avec une petite zone de stockage pour des colis sur cette plateforme. Un projet très intéressant pour des étudiants seraient alors de calculer les mouvements du robot permettant d'amener les plus rapidement possibles une liste de colis présents dans un entrepôt au point de chargement des camions de livraison. 


**Mots clés du projet:** 

- `Bin Packing`: La plateforme du robot ne possède qu'un certain volume. Il est donc nécessaire d'utiliser des algorithme d'optimisation permettant de réfléchir à l'ordre dans lequel les colis vont être récupérés car chaque colis possède son propre poids et son propre volume. Un problème d'optimisation bien connu lié à cette question est le problème du [Bin Packing](https://en.wikipedia.org/wiki/Bin_packing_problem).


- `Graphes et Plus courts chemins`: L'entrepôt peut être modélisé mathématiquement comme un graphe: la présence d'autres robots ou d'obstacles obstruant un passage peut rendre certains chemins impossibles à emprunter pour notre robot. De ce fait, utiliser des algorithmes permettant le calcul de plus courts chemins dans les graphes peut être pertinent dans ce contexte.

- `Ordonnancement`: 
