# from rest_framework import serializers
# from .models import Review, Comment

        
# class ReviewSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = Review
#         fields = ('id','title', 'movie', 'content', 'rank', 'user', 'like_users', 'created_at', 'updated_at')
#         read_only_fields = ('user', 'created_at', 'updated_at', 'like_users')

# class ReviewLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ('like_users')

# class ReviewCreationSerializer(serializers.ModelSerializer): 
#     like_users = ReviewLikeSerializer(many=True, read_only=True)
#     class Meta:
#         model = Review
#         fields = '__all__'

# class CommentSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = Comment
#         fields = ('id','content','user')

# class CommentListSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = Comment
#         fields = '__all__'