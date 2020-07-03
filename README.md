# APP ERO: Déneigeons Montreal !  
  
## Installation  
  
Ce projet necessite le programme python3 ainsi que le gestionnaire de paquets pip3.  
  
### Linux  
  
Afin de lancer la commande suivante le paquet python3-venv est requis.  
  
```js  
./setup.sh  
```  
  
De plus, il faut installer le paquet spatialindex afin qu'OSMnx puisse fonctionner.  
  
### Windows  
  
```js  
pip3 install -r requirements.txt  
```  
  
Cette commande permet d'installer les paquets nécessaires à l'execution du projet à savoir: numpy, scipy et osmnx  
  
  
## Exemple d'utilisation  
  
  
```js  
$ python3 snowymontreal.py  
> Type "drone" or "snow plow" depending on what you want to use: drone  
> Latitude of drone: 45.501690  
> Longitude of drone: -73.567253  
> Radius for drone to cover: 300  
```  
  
## Moteur de notre solution  
  
Le moteur de notre solution se trouve dans le module _snowymontreal_.  
  
Nous pouvons y trouver plusieurs fonctions permettant de répondre au problème, à savoir calculer le chemin minimal parcourant toutes les arêtes du graphe en entrée.  
  
 - La fonction que nous avons codée au maximum avec nos algorithmes est la fonction principale de notre moteur: *solve*. Elle s'appuie sur les bibliothèques numpy, ainsi que scipy qui nous permet d'utiliser la programmation linéaire afin de trouver le couplage parfait minimum dans un graphe biparti.  
 - Une variante de notre fonction principale est la fonction *optimized_solve*. La seule différence entre cette variante et la fonction *solve* est la résolution du problème dans le cas d'un graphe non orienté. Nous utilisons dans cette variante la bibliothèque networkx qui nous permet de trouver le couplage minimum dans un graphe quelconque. Le déroulé de l'algorithme est le même sauf qu'au lieu de calculer l'arbre couvrant minimal et de chercher le couplage sur celui-ci, nous calculons directement le couplage minimal dans le graphe de départ grâce à la bibliothèque networkx. Cette variante donne donc un chemin dont le coût est garanti d'être minimal contrairement à l'autre qui donne seulement une approximation du chemin minimal.  
 - Pour finir nous avons les fonctions *snow_plow_solve* et *drone_solve* qui, à partir de la position de départ de la déneigeuse ou du drone, calcule le chemin minimal pour parcourir toutes les arêtes. Nous utilisons ces fonctions pour l'interfaçage avec OSMnx et donc pour résoudre le problème sur des graphes de taille importante. Nous utilisons les mêmes bibliothèques que pour la fonction *optimized_solve* sauf que nous utilisons plus d'algorithmes de la bibliothèque networkx.  
  
## Interfaçage avec OSMnx  
  
Afin de répondre au maximum à la problèmatique de départ (Déneiger Montréal), nous avons interfacé notre moteur avec la bibliotèque OSMnx. Pour cela, nous demandons à l'utilisateur de rentrer comme information si il veut utiliser le drone ou la déneigeuse. Une fois sélectionné, il devra choisir la position de départ du drone/déneigeuse ainsi que le rayon d'action autour de la position. Une fois toute ces informations entrées, le graphe de la zone d'action s'affichera et le chemin calculé pour le drone ou la déneigeuse se dessinera au fur et à mesure. Cela répond à la problématique dans le sens où, en fonction du matériel que la ville de Montréal a à disposition (drone et déneigeuse), ils pourront executer notre solution pour chaque drone/déneigeuse sur un certain rayon d'action et donc répartir la charge de travail en fonction du nombre d'appareil.
