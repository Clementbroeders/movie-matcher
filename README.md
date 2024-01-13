# MOVIE MATCHER

## Notebooks :

1) `01_TMDB_API_movie_vote.ipynb` : Télécharge le daily export de TMDB, filtre sur les `n` films les plus populaires, puis se connecte à l'API TMDB pour récupérer par film le nombre de votes et la moyenne des votes. Ensuite enregistre dans le fichier `src/TMDB_movie_vote.csv`. 

Temps de traitement : 2min30 pour 1000 films.

2) `02_weighted_IMDB.ipynb` : Parmi les films de `src/TMDB_movie_vote.csv`, applique la formule weighted ratings de IMDB et déduit une liste de `n` films les mieux notés. Ensuite enregistre dans le fichier `src/TMDB_weighted_movies.csv`. De plus, importe `Movielens_links.csv` et `Movielens_ratings.csv`, filtre sur les films sélectionnés, puis effectue un sample pour limiter la taille du dataset. Enregistre les infos dans le fichier `src/Movielens_ratings_updated.csv`.

3) `03_TMDB_API_content.ipynb` : Parmi les films de `src/TMDB_weighted_movies.csv`, se connecte à l'API TMDB pour récupérer, par film, les données suivantes :
    - TMDB/movie/details : TMDB_id, title, genres
    - TMDB/movie/keywords : TMDB_id, keywords
    - TMDB/movie/credits : TMDB_id, cast (acteurs)

Temps de traitement : 36 min pour 2000 films

4) `04_collaborative_filtering.ipynb` : Défini la fonction de recommandation (collaborative filtering) à partir de la librairie Suprise et du modèle SVD, puis la teste sur une liste de films.

Idéalement entre 100.000 et 500.000 ratings.

---
## Instructions si aucun fichier n'est présent dans `src/` :

1) Telecharger le dataset MovieLens : [Movielens dataset](https://files.grouplens.org/datasets/movielens/ml-latest.zip)

2) Deziper l'archive
    Renommer : `ratings.csv` en `Movielens_ratings.csv`
    Renommer : `links.csv` en `Movielens_links.csv`
    Mettre les fichiers dans `src/`

3) Lancez les notebooks `01`, `02` et `03` pour créer les fichiers nécessaires au machine learning