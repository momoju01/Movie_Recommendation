from django.db.models.expressions import OrderBy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.http import require_safe
from .models import Movie, Genre, Review, Comment
from .forms import ReviewForm, CommentForm
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required


# from django.core.paginator import Paginator
from django.db.models import Q
from random import choice, randint
import random

# Create your views here.


def home(request):
    # 메인에 띄울 동영상(최신 흥행중 랜덤)
    recent_movies = Movie.objects.order_by('-release_date')[:10]
    random_movie = random.choice(recent_movies)
    context = {
        'random_movie': random_movie,
    }
    return render(request, 'movies/home.html', context)


@require_safe
def index(request):
    # 흥행작
    popular_movies = Movie.objects.order_by('-popularity')[:4]
    popular_movies_2 = Movie.objects.order_by('-popularity')[4:8]
    
    # 장르별 영화 추천(장르별로 장르가 들어간 영화 dict형태로 list에 추가)
    genres = Genre.objects.all()
    genre_movies = []
    genre_movies_2 = []
    for genre in genres:
        genre_movies.append({
            genre.name: Movie.objects.filter(genre_ids__in=[genre.id])[:4]
        })
        genre_movies_2.append({
            genre.name: Movie.objects.filter(genre_ids__in=[genre.id])[4:8]
        })

    # 내 취향 장르 기반
    rec_movie_genres = []
    rated_movies = []
    if request.user.is_authenticated:
        if Review.objects.filter(user_id=request.user.id).count():
            reviews = Review.objects.filter(user_id=request.user.id) #유저가 작성한 리뷰 중
            top_review = reviews.filter(Q(rank=4)|Q(rank=5)).order_by('-rank')[0]  # 평가 높은 리뷰들
            like_movie_genres = top_review.movie.genre_ids.all()  # 리뷰 높은 영화의 장르들
            for like_movie_genre in like_movie_genres: 
                rec_movie_genres.append({
                    like_movie_genre.name: Movie.objects.filter(genre_ids__in=[like_movie_genre.id])[:8]
                })
            
        else: # 작성한 리뷰 없는 경우 평점순
            rated_movies = Movie.objects.order_by('-vote_average')[:8]
    else: # 로그인 안 한 경우 평점순
        rated_movies = Movie.objects.order_by('-vote_average')[:8]
    context = {
        'popular_movies': popular_movies,
        'popular_movies_2': popular_movies_2,
        'genre_movies': genre_movies,
        'genre_movies_2': genre_movies_2,
        'rec_movie_genres': rec_movie_genres,
        'rated_movies': rated_movies[:4],
        'rated_movies_2': rated_movies[4:8],
    }
    return render(request, 'movies/index.html', context)



@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # genres = movie.movie_genre.all()  #역참조 / genre가 선택된 것이 여러개가 있을 수 있으므로! / 중개테이블 안에 있는 것을 모두 들고옴 / 여러개의 장르들! for문
    genre_ids = movie.genre_ids.all()  
    reviews = movie.reviews.all()
    context = {
        'movie':movie,
        'genre_ids':genre_ids,
        'reviews': reviews,
    }
    return render(request, 'movies/detail.html', context)
    
    

@require_http_methods(['GET', 'POST'])
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST) 
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies:detail', movie_pk)
    else:
        review_form = ReviewForm()
    context = {
        'review_form': review_form,
        'movie': movie,
        'reviews': movie.reviews.all()
    }
    return render(request, 'movies/create.html', context)



@require_GET
def review_detail(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'movie': movie,
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'movies/review.html', context)



@login_required
@require_http_methods(['GET', 'POST'])
def review_update(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, instance=review)
            if review_form.is_valid():
                review_form.save()
                return redirect('movies:review_detail', movie.pk, review.pk)
        else:
            review_form = ReviewForm(instance=review)
    else:
        return redirect('movies:index')
    context = {
        'review': review,
        'review_form': review_form,
        'movie': movie,
    }
    return render(request, 'movies/update.html', context)

@require_POST
def review_delete(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.user.is_authenticated:
        if request.user == review.user: 
            review.delete()
            return redirect('movies:detail', movie.pk)
    return redirect('movies:review_detail', movie.pk, review.pk)




@require_POST
def create_comment(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('movies:review_detail', movie.pk, review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
        'movie': movie,
    }
    return render(request, 'movies/review.html', context)


@require_POST
def comment_delete(request, movie_pk, review_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:review_detail', movie_pk, review_pk)


@require_POST
def like_review(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            # 좋아요 여부
            liked = False
        else:
            review.like_users.add(user)
            # 좋아요 여부
            liked = True

        like_status = {
            'liked':liked,
            'count':review.like_users.count(),
        }
        # return redirect('community:index')
        return JsonResponse(like_status)    #좋아요상태를담아서보내줄것
    # return redirect('accounts:login')
    return HttpResponse(status=401) #401이 에러인데,
    #403은 권한(인가)없다, 401은 로그인(인증)이 안되었다, 403은 못들어감







# @require_safe
# def recommended(request):
#     rec_movies = Movie.objects.order_by('-vote_average')[:8]
#     # rec_movies = Movie.objects.all()[randint(0, 5)]
#     context = {
#         'rec_movies':rec_movies,
#     }
#     return render(request, 'movies/recommended.html', context)


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

