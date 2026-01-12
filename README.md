### API environment

cd Api

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt







### Module environment
cd ../Module

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt





### Run the FastAPI API
cd ../Api

source venv/bin/activate

uvicorn Api:app --reload






### Docker
docker build -t movie-recommender .

docker run -p 8000:8000 movie-recommender





### test the API
curl -X POST \
  'http://127.0.0.1:8000/recommend-hybrid' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": 196,
    "title": "Toy Story"
  }'

