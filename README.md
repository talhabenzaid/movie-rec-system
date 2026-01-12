cd Api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../Module
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../Api
source venv/bin/activate
uvicorn Api:app --reload

docker build -t movie-recommender .
docker run -p 8000:8000 movie-recommender

curl -X POST \
  'http://127.0.0.1:8000/recommend-by-movie' \
  -H 'Content-Type: application/json' \
  -d '{"title": "Toy Story"}'

