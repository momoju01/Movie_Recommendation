from django.db.models import fields
from rest_framework import serializers

from accounts.serializers import User
from community.models import Comment, Review
from .models import Movie, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Genre
        fields = ('name',)

class MovieSerializer(serializers.ModelSerializer):
    genre_ids = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
    
class ProfileMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path')

class ReviewUserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)

class CommunityCommentSerializer(serializers.ModelSerializer):
    user = ReviewUserCommentSerializer()

    class Meta:
        model = Comment
        fields = '__all__'

class ReviewListSerializer(serializers.ModelSerializer):
    review_comments = CommunityCommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='review_comments.count', read_only=True)
    user = ReviewUserCommentSerializer()

    class Meta:
        model = Review
        fields = ('id', 'review_comments', 'content', 'comment_count', 'rank', 'movie', 'title')
