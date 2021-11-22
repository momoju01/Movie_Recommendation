from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/create/', views.review_create, name='review_create'), 
    path('<int:movie_pk>/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:movie_pk>/<int:review_pk>/update/', views.review_update, name='review_update'),
    path('<int:movie_pk>/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:movie_pk>/<int:review_pk>/comments/create/', views.create_comment, name='create_comment'),
    path('<int:movie_pk>/<int:review_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:review_pk>/like_review/', views.like_review, name='like_review'),
]
