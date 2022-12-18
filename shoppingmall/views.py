from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Toy, Category, Material, Maker, Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['title', 'hook_text', 'content', 'head_image', 'price', 'maker', 'category']
    template_name = 'shoppingmall/toy_update_form.html'      # 템플릿을 호출

    # 포스트를 작성한 유저 확인
    def dispatch(self, request, *args, **kwargs):
        # request 유저와 post를 작성한 유저가 같은지 확인
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ToyUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied          # PermissionDenied exception 발생시킴

    # post방식으로 전달하면 form_valid()가 필요함
    def form_valid(self, form):
        response = super(ToyUpdate, self).form_valid(form)
        self.object.material.clear()
        tags_str = self.request.POST.get('tags_str')  # toy_form의 tags_str을 가져옴
        if tags_str:
            tags_str = tags_str.strip()  # 문자열의 앞 뒤 공백 제거
            tags_str = tags_str.replace(',', ';')  # 구분자(delimiter) ;로 통일
            tags_list = tags_str.split(';')  # ex) 'internet; programming;' -> 'internet' 'programming'

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Material.objects.get_or_create(name=t)  # 문자열에 해당하는 태그 객체 없으면 create, 있으면 가져옴
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)  # 새로 생성된 태그의 경우, 슬러그 생성
                    tag.save()
                self.object.material.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ToyUpdate, self).get_context_data()

        # 기존 post에 tag가 있는 경우
        if self.object.material.exists:
            tag_str_list = list()
            for t in self.object.material.all():
                tag_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tag_str_list)
        context['categories'] = Category.objects.all()
        context['makers'] = Maker.objects.all()
        context['materials'] = Material.objects.all()
        context['no_category_post_count'] = Toy.objects.filter(category=None).count

        return context

class ToyCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Toy
    fields = ['title', 'hook_text', 'content', 'head_image', 'price', 'maker', 'category', 'material']

    # 모델명_form.html이 자동으로 호출

    # 슈퍼유저 or 스태프유저에게 접근권한 부여(모델에 대한)
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user            # 현재 post를 생성하는 유저
        if current_user.is_authenticated and \
                (current_user.is_superuser or self.request.user.is_staff):            # 해당 유저가 인증된 유저이면
            form.instance.author = current_user     # 폼의 authorm를 해당 유저로
            response = super(ToyCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')     # toy_form의 tags_str을 가져옴

            if tags_str:
                tags_str = tags_str.strip()     # 문자열의 앞 뒤 공백 제거
                tags_str = tags_str.replace(',', ';')      # 구분자(delimiter) ;로 통일
                tags_list = tags_str.split(';')            # ex) 'internet; programming;' -> 'internet' 'programming'

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Material.objects.get_or_create(name=t)       # 문자열에 해당하는 태그 객체 없으면 create 있으면 가져옴
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)           # 새로 생성된 태그의 경우, 슬러그 생성
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/shopping/')        #인증되지 않은 사용자일 경우 그냥 redirect

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ToyCreate, self).get_context_data()

        context['makers'] = Maker.objects.all()
        context['materials'] = Material.objects.all()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Toy.objects.filter(category=None).count

        return context

# Create your views here.
class ToyList(ListView):
    model = Toy
    ordering = '-pk'   # pk로 내림차순으로 정렬(최신순)
    paginate_by = 6     # 한 페이지에 9개씩 보여줌

    # ToyList에서 사용할 데이터를 넘겨줌(여기서는 카테고리)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ToyList, self).get_context_data()
        context['makers'] = Maker.objects.all()
        context['materials'] = Material.objects.all()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Toy.objects.filter(category=None).count

        return context


class ToyDetail(DetailView):
    model = Toy

    def get_context_data(self, **kwargs):
        context = super(ToyDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['makers'] = Maker.objects.all()
        context['materials'] = Material.objects.all()
        context['no_category_post_count'] = Toy.objects.filter(category=None).count
        context['comment_form'] = CommentForm
        return context

# 댓글 수정을 위한 뷰
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    # 템플릿 이름: comment_form
    template_name = 'shoppingmall/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        # request 유저와 comment를 작성한 유저가 같은지 확인
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied          # PermissionDenied exception 발생시킴

    # ToyList에서 사용할 데이터를 넘겨줌(여기서는 카테고리)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CommentUpdate, self).get_context_data()
        context['makers'] = Maker.objects.all()
        context['materials'] = Material.objects.all()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Toy.objects.filter(category=None).count

        return context

# 댓글 등록하는 메소드
def new_comment(request, pk):
    if request.user.is_authenticated:       # 로그인한 유저인가
        toy = get_object_or_404(Toy, pk=pk)       # 해당 댓글이 달린 포스트 가져옴
        if request.method == 'POST':                # 새로 댓글을 작성하는 경우
            comment_form = CommentForm(request.POST)        # POST로 전달받은 내용
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)   # 모델에 등록(commit)은 하지 않음
                comment.toy = toy
                comment.author = request.user
                comment.save()              # 모델에 등록
                return redirect(comment.get_absolute_url())
        else:   # request.method == 'GET'인 경우
            return redirect(toy.get_absolute_url())
    else:       # 로그인하지 않은 유저인 경우
        raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    toy = comment.toy

    # 인증된 사용자인지
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()        # 댓글 삭제
        return redirect(toy.get_absolute_url())

    else:
        PermissionDenied

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
        'makers': Maker.objects.all(),
        'materials': Material.objects.all(),
        'categories': Category.objects.all(),
        'no_category_post_count': Toy.objects.filter(category=None).count
    })

def material_page(request, slug):
    material = Material.objects.get(slug=slug)
    toy_list = material.toy_set.all()          # tag값을 가진 포스트 집합

    return render(request, 'shoppingmall/toy_list.html', {
        'material': material,
        'toy_list': toy_list,
        'makers': Maker.objects.all(),
        'materials': Material.objects.all(),
        'categories': Category.objects.all(),
        'no_category_post_count': Toy.objects.filter(category=None).count
    })

def maker_page(request, pk):
    maker = Maker.objects.get(pk=pk)
    toy_list = maker.toy_set.all()          # tag값을 가진 포스트 집합

    return render(request, 'shoppingmall/toy_list.html', {
        'maker': maker,
        'toy_list': toy_list,
        'makers': Maker.objects.all(),
        'materials': Material.objects.all(),
        'categories': Category.objects.all(),
        'no_category_post_count': Toy.objects.filter(category=None).count
    })

# 검색
class ToySearch(ToyList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']            # 검색어(query)를 가져 옴

        # 포스트 제목과 내용에 대해 검색
        toy_list = Toy.objects.filter(Q(title__contains=q) | Q(content__contains=q)).distinct()

        return toy_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ToySearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'{q}'
        context['search_count'] = f'{self.get_queryset().count()}'
        return context