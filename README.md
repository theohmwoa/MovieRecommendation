# Bienvenue sur le projet Movie recommendation

Ce projet vous permet d'utiliser les données de MovieLens pour différentes analyses et applications. Suivez les instructions ci-dessous pour mettre en place l'environnement et lancer l'application.

## Étape 1: Télécharger le dataset MovieLens

Avant toute chose, vous aurez besoin des données MovieLens. Vous pouvez télécharger le dataset depuis l'URL suivante:

```
https://grouplens.org/datasets/movielens/latest/
```

Choisissez le fichier qui correspond le mieux à vos besoins (par exemple, `ml-latest-small.zip` pour un ensemble de données plus petit et plus gérable).

## Étape 2: Prétraitement des données

Après avoir téléchargé le dataset, décompressez le fichier dans le répertoire de votre choix. Ensuite, accédez au dossier `PreProcess` de ce projet.

Lancez le script `main` avec la commande suivante :

```bash
python main.py
```

Assurez-vous que toutes les dépendances nécessaires sont installées avant de lancer le script. Ce script va préparer les données pour une utilisation ultérieure par l'API et l'interface web.

## Étape 3: Lancer l'API

Une fois que vous avez prétraité les données, vous pouvez démarrer l'API. Pour cela, accédez au dossier de l'API et suivez les instructions spécifiques à l'API pour la lancer (les instructions seront probablement disponibles dans un fichier `README` dans le dossier de l'API).

## Étape 4: Lancer l'interface web

Enfin, pour lancer l'interface web, vous devrez installer les dépendances nécessaires. Ouvrez un terminal, accédez au dossier web et exécutez les commandes suivantes :

```bash
cd web
npm install
npm start
```

Ces commandes vont installer toutes les dépendances nécessaires et démarrer le serveur web. Une fois le serveur lancé, vous pouvez accéder à l'interface via votre navigateur web en allant à l'adresse indiquée dans la console (habituellement `http://localhost:3000`).
