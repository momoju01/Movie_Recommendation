from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from .models import Movie, Genre
from random import randint


# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    
    context = {
        'movies': movies
    }
    return render(request, 'movies/index.html', context)



@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    # genres = movie.movie_genre.all()  #역참조 / genre가 선택된 것이 여러개가 있을 수 있으므로! / 중개테이블 안에 있는 것을 모두 들고옴 / 여러개의 장르들! for문
    genres = movie.genres.all()  #역참조 / genre가 선택된 것이 여러개가 있을 수 있으므로! / 중개테이블 안에 있는 것을 모두 들고옴 / 여러개의 장르들! for문
    print(genres)
    # <QuerySet [<Genre: 애니메이션>, <Genre: 드라마>, <Genre: 로맨스>]>
    # comments = movie.comment_set.all()
    context = {
        'movie':movie,
        'genres':genres,
    }
    return render(request, 'movies/detail.html', context)
    
    

@require_safe
def recommended(request):
    rec_movies = Movie.objects.order_by('-vote_average')[:8]
    # rec_movies = Movie.objects.all()[randint(0, 5)]
    context = {
        'rec_movies':rec_movies,
    }
    return render(request, 'movies/recommended.html', context)