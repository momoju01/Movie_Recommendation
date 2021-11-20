from django import forms
from .models import Review, Comment
# Create your forms here.




class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        # fields = ['title', 'movie_title', 'rank', 'content']
        fields = ['title', 'rank', 'content']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['review', 'user']

