from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe
from .models import Movie, Genre
# from django.core.paginator import Paginator
from random import randint


"""
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('recommended/', views.recommended, name='recommended'),
"""

# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    # print(movies) 
    """
    <QuerySet [<Movie: 가브리엘의 지옥 파트 2>, <Movie: 가브리엘의 지옥>, <Movie: Dedicada a mi ex>, <Movie: 쇼생크 탈출>, <Movie: 
    용감한 자가 신부를 데려가리>, <Movie: 대부>, <Movie: 쉰들러 리스트>, <Movie: 나의 히어로 아카데미아 더 무비: 히어로즈 라이징>, <Movie: 너의 이름은.>, <Movie: 대부 2>, <Movie: 센과 치히로의 행방불명>, <Movie: 기생충>, <Movie: 해밀턴>, <Movie: 우리는 그토록 
    사랑했네>, <Movie: 그린 마일>, <Movie: 펄프 픽션>, <Movie: 인생은 아름다워>, <Movie: 반지의 제왕: 왕의 귀환>, <Movie: 다크 나이 
    트>, <Movie: 12명의 성난 사람들>, '...(remaining elements truncated)...']>
    """
    # paginator = Paginator(movies, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    context = {
        'movies': movies
        # 장르가 많으니까, 역참조로 따로 
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


# # random으로 추천
# import random
# @require_safe
# def recommended(request):
#     movies_list = list(Movie.objects.all())
#     random_movies_list = random.sample(movies_list, 8)
#     print(random_movies_list)
#     """
#     [<Movie: 어벤져스: 엔드게임>, <Movie: 동경 이야기>, <Movie: 양들의 침묵>, <Movie: 하울의 움직이는 성>, <Movie: 시티 오브 갓>, <Movie: 기생충>, <Movie: 마미>, <Movie: 잠입자>]
#     [<Movie: 콜 미 바이 유어 네임>, <Movie: 아메리칸 히스토리 X>, <Movie: 마돈나 거리에서 한탕>, <Movie: 좋은 친구들>, <Movie: 자전거 도둑>, <Movie: 8과 1/2>, <Movie: 양들의 침묵>, <Movie: 드래곤 길들이기: 홈커밍>]
#     """
#     context = {
#         'rec_movies':random_movies_list,
#     }
#     return render(request, 'movies/recommended.html', context)