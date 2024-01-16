### LIBRAIRIES ###
import uvicorn
import pandas as pd 
from fastapi import FastAPI
from pydantic import BaseModel
from surprise import Dataset, Reader, SVD


### APP ###
app = FastAPI()


### LOAD FILES ###
ratings_updated = pd.read_csv('data/Movielens_ratings_updated.csv')
# content_based = pd.read_csv('data/content_based.csv')


### FONCTIONS ###
class RecommendationRequest(BaseModel):
    favorite_movies: list


### GET ###
@app.get("/")
async def index():

    message = "Bienvenue sur notre API. Ce '/' est l'endpoint le plus simple et celui par défaut. Si vous voulez en savoir plus, consultez la documentation de l'api à '/docs'"

    return message

### POST ###
@app.post("/predict")
async def predict(recommendation_request: RecommendationRequest):
    global ratings_updated

    favorite_movies = recommendation_request.favorite_movies

    ### COLLABORATIVE FILTERING ###
    new_user_id = ratings_updated['userId'].max() + 1

    for i in favorite_movies:
        newdata = pd.DataFrame([[new_user_id, i, 5.0]], columns=['userId', 'tmdb_id', 'rating'])
        ratings_updated = pd.concat([ratings_updated, newdata], ignore_index=True)

    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(ratings_updated[['userId', 'tmdb_id', 'rating']], reader)
    svd = SVD()
    train_set = data.build_full_trainset()
    svd.fit(train_set)

    all_pred = []
    movie_id = []
    for movie in ratings_updated['tmdb_id'].unique().tolist():
        pred = svd.predict(new_user_id, movie)
        all_pred.append(pred.est)
        movie_id.append(pred.iid)

    result = pd.DataFrame(list(zip(movie_id, all_pred)), columns=['tmdb_id', 'predicted_rating'])
    result.sort_values(by='predicted_rating', ascending=False, inplace=True)

    return result.to_dict(orient='records')


### RUN APP ###
if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) # Here you define your web server to run the `app` variable (which contains FastAPI instance), with a specific host IP (0.0.0.0) and port (4000)