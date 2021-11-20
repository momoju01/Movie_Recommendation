from django.shortcuts import render
from movies.models import Review
from django.views.decorators.http import require_GET
# Create your views here.

@require_GET
def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews,
    }
    return render(request, 'community/index.html', context)