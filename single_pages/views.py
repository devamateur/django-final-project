from django.shortcuts import render

# Create your views here.
from shoppingmall.models import Toy, Comment

def landing(request):
    recent_toy = Toy.objects.order_by('-pk')[:3]      # 포스트를 최신순으로 3개 가져 옴
    return render(request, 'single_pages/landing.html', {
        'recent_toys': recent_toy,
    })

def about_us(request):
    return render(request, 'single_pages/about_us.html')

def mypage(request):

    comment = Comment.objects.filter(author=request.user)
    comment.author = request.user

    toy_list = Toy.objects.filter(author=comment.author)

    return render(request, 'single_pages/mypage.html', {
        'comment': comment,
        'toy_list': toy_list
    })