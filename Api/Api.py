from fastapi import FastAPI
from pydantic import BaseModel
import pickle

app = FastAPI()

with open('recommender_models.pkl', 'rb') as f:
    models = pickle.load(f)

cosine_sim = models['cosine_sim']
indices = models['indices']
movies_unique = models['movies_unique']
predictions_df = models['predictions_df']
user_matrix = models['user_matrix']

class MovieRequest(BaseModel):
    title: str

class UserRequest(BaseModel):
    user_id: int

class HybridRequest(BaseModel):
    title: str
    user_id: int

def content_based(title, cosine_sim):
    if title not in indices:
        return []
    idx = indices[title]
    scores = cosine_sim[idx]
    sim_scores = []
    for i in range(len(scores)):
        sim_scores.append((i, scores[i]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = []
    for i in sim_scores:
        movie_indices.append(i[0])
    return movies_unique['title'].iloc[movie_indices].tolist()

def collaborative_recommender(user_id):
    if user_id not in user_matrix.index:
        return []
    user_idx = user_matrix.index.get_loc(user_id)
    user_ratings = user_matrix.iloc[user_idx]
    user_predictions = predictions_df.iloc[user_idx]
    unwatched_movies = user_ratings[user_ratings == 0].index
    recommendations = user_predictions[unwatched_movies].sort_values(ascending=False)
    top_movies = recommendations.head(10).index
    result = movies_unique[movies_unique['movie_id'].isin(top_movies)]['title'].tolist()
    return result

def hybrid(title, user_id, cosine_sim):
    content_recs = content_based(title, cosine_sim)
    collab_recs = collaborative_recommender(user_id)
    
    unique_collab = []
    for movie in collab_recs:
        if movie not in content_recs:
            unique_collab.append(movie)
    
    final_recs = content_recs[:5] + unique_collab[:5]
    
    return final_recs

@app.get("/")
def root():
    return {"message": "Movie Recommender API"}

@app.get("/movies")
def get_movies():
    return {"movies": movies_unique['title'].tolist()}

@app.post("/recommend-by-movie")
def rec_movie(request: MovieRequest):
    recommendations = content_based(request.title, cosine_sim)
    if not recommendations:
        return {"error": f"Movie '{request.title}' not found"}
    return {"recommendations": recommendations}

@app.post("/recommend-by-user")
def rec_user(request: UserRequest):
    recommendations = collaborative_recommender(request.user_id)
    if not recommendations:
        return {"error": f"User {request.user_id} not found"}
    return {"recommendations": recommendations}

@app.post("/recommend-hybrid")
def rec_hybrid(request: HybridRequest):
    recommendations = hybrid(request.title, request.user_id, cosine_sim)
    if not recommendations:
        return {"error": "No recommendations found"}
    return {"recommendations": recommendations}