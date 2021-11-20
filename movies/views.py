from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.http import require_safe
from .models import Movie, Genre, Review, Comment
from .forms import ReviewForm, CommentForm
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required

# from django.core.paginator import Paginator
from random import randint


"""
app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'), #detail > movie_detail
    path('<int:movie_pk>/create/', views.create_review, name='create_review'), #
    path('<int:movie_pk>/<int:review_pk>/', views.review_detail, name='review_detail'),#
    path('<int:movie_pk>/<int:review_pk>/comments/create/', views.create_comment, name='create_comment'),#
    path('<int:movie_pk>/<int:review_pk>/like/', views.like, name='like'),
    path('recommended/', views.recommended, name='recommended'),
]

"""

# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
        # 장르가 많으니까, 역참조로 따로 
    }
    return render(request, 'movies/index.html', context)



@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # genres = movie.movie_genre.all()  #역참조 / genre가 선택된 것이 여러개가 있을 수 있으므로! / 중개테이블 안에 있는 것을 모두 들고옴 / 여러개의 장르들! for문
    genre_ids = movie.genre_ids.all()  #역참조 / genre가 선택된 것이 여러개가 있을 수 있으므로! / 중개테이블 안에 있는 것을 모두 들고옴 / 여러개의 장르들! for문
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


def recommended(request):
    """
     영화목록중 vote_average가 8 이상인 영화목록 출력.
    """
    reviews = Review.objects.all()

    movies_gt_8 = []
    for review in reviews:
        if review['rank'] >= 4:
            movies_gt_8.append(review.movie)
    context = {
        'movies_gt_8': movies_gt_8,
    }
    return render(request, 'movies/recommended.html', context)


# if __name__ == '__main__':
#     pprint(rated_movies())