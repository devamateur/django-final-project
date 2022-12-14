from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Toy, Category

# Create your views here.
class ToyList(ListView):
    model = Toy
    ordering = '-pk'   # pk로 내림차순으로 정렬(최신순)
    paginate_by = 5     # 한 페이지에 5개씩 보여줌

    # ToyList에서 사용할 데이터를 넘겨줌(여기서는 카테고리)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ToyList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Toy.objects.filter(category=None).count

        return context


class ToyDetail(DetailView):
    model = Toy

    # 템플릿 -> post_detail.html이 자동으로 불려짐
    # 전달되는 매개변수: 모델명 -> post