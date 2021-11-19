# from django.db.models import fields
# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User = get_user_model()

# from community.serializers import CommentListSerializer, ReviewSerializer
# from movies.serializers import ProfileMovieSerializer

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True) # 읽기 only

#     class Meta:
#         model = User
#         fields = ('username', 'password',)

# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username')


# class UserProfileSerializer(serializers.ModelSerializer):
#     reviews = ReviewSerializer(many=True, read_only=True)
#     comments = CommentListSerializer(many=True, read_only=True)

#     like_movies = ProfileMovieSerializer(many=True, read_only=True)
#     like_reviews = ReviewSerializer(many=True, read_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'reviews', 'comments', 'like_movies', 'like_reviews')