# Depuis1958

Modèle statistique du scrutin uninominal majoritaire à deux tours de l'élection
présidentielle française, inspiré par FiveThirtyEight (et d'autres).

## Utiliser le modèle Python

Le point d'entrée est la classe `ElectionModel` (dans `election.py`) qui
modélise la probabilité totale de victoire.

## Générer le site web complet

Le site web est basé sur des templates Jinja2. Tout est automatisé. Pour le
générer, créer un symlink vers les sondages. Les miens sont ici: https://github.com/depuis1958/sondages :

    ln -s ../sondages/presidentielle/ data

Ensuite, le script `page.py` fait tout le boulot :

    ./page.py

et génère un répertoire "public" avec le contenu html.
