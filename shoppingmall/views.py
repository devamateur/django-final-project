from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Toy, Category, Material, Maker

# Create your views here.
class ToyList(ListView):
    model = Toy
    ordering = '-pk'   # pk로 내림차순으로 정렬(최신순)
    paginate_by = 6     # 한 페이지에 9개씩 보여줌

    # ToyList에서 사용할 데이터를 넘겨줌(여기서는 카테고리)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ToyList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Toy.objects.filter(category=None).count

        return context


class ToyDetail(DetailView):
    model = Toy

    def get_context_data(self, **kwargs):
        context = super(ToyDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Toy.objects.filter(category=None).count
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        toy_list = Toy.objects.filter(category=None)
    else:
        # 특정 slug를 갖는 카테고리
        category = Category.objects.get(slug=slug)
        toy_list = Toy.objects.filter(category=category)

    return render(request, 'shoppingmall/toy_list.html', {
        'category': category,
        'toy_list': toy_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Toy.objects.filter(category=None).count
    })

def material_page(request, slug):
    material = Material.objects.get(slug=slug)
    toy_list = material.toy_set.all()          # tag값을 가진 포스트 집합

    return render(request, 'shoppingmall/toy_list.html', {
        'material': material,
        'toy_list': toy_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Toy.objects.filter(category=None).count
    })

def maker_page(request, pk):
    maker = Maker.objects.get(pk=pk)
    toy_list = maker.toy_set.all()          # tag값을 가진 포스트 집합

    return render(request, 'shoppingmall/toy_list.html', {
        'maker': maker,
        'toy_list': toy_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Toy.objects.filter(category=None).count
    })