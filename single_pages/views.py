from django.shortcuts import render

# Create your views here.
from shoppingmall.models import Toy

def landing(request):
    recent_toy = Toy.objects.order_by('-pk')[:3]      # 포스트를 최신순으로 3개 가져 옴
    return render(request, 'single_pages/landing.html', {
        'recent_toys': recent_toy,
    })

def about_us(request):
    return render(request, 'single_pages/about_us.html')