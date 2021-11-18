# # 영화정보를 API를 이용해서 가져오기
import json
import requests
# from api_key import URLMaker
from decouple import config
MOVIE_API_KEY = config('API_KEY')



# 1. movie 정보
result = []
url = 'https://api.themoviedb.org/3/movie/popular'
key = MOVIE_API_KEY
for page in range(1, 6):
    URL = f'{url}?api_key={key}&language=ko-Kr&page={page}'

    raw_data = requests.get(URL).json()
    data = raw_data.get('results')
    for movie in data:
        movie_dict = {
            "model" : "movies.movie",
            "pk" : movie.get("id"),
            "fields" : {
                "title" : movie.get("title"),
                "popularity" : movie.get("popularity"),
                "genre_ids" : movie.get("genre_ids"),
                "release_date" : movie.get("release_date"),
                "vote_average" : movie.get("vote_average"),
                "vote_count" : movie.get("vote_count"),
                "overview" : movie.get("overview"),
                "poster_path" : movie.get("poster_path")
            }
        }
        result.append(movie_dict)



with open('movies.json', 'w', encoding='UTF-8') as file:
    file.write(json.dumps(result, ensure_ascii=False))


## 2. genre 정보
result = []
genre_url = 'https://api.themoviedb.org/3/genre/movie/list'
key = MOVIE_API_KEY
GENRE_URL = f'{genre_url}?api_key={key}&language=ko-Kr'
# https://api.themoviedb.org/3/genre/movie/list?api_key=<<api_key>>&language=en-US

raw_data = requests.get(GENRE_URL).json()
data = raw_data.get('genres')

for genre in data:
    genre_dict = {
        "model" : "movies.genre",
        "pk" : genre.get("id"),
        "fields" : {
            "name" : genre.get("name")
        }
    }
    result.append(genre_dict)

with open('genres.json', 'w', encoding='UTF-8') as file:
    file.write(json.dumps(result, ensure_ascii=False))
