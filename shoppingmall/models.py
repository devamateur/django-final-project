from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

# Material - 다대다
class Material(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):  # 객체에 대한 문자열 리턴
        return self.name

    def get_absolute_url(self):
        return f'/shopping/material/{self.slug}/'

# Maker, Category - 다대일
class Maker(models.Model):
    name = models.CharField(max_length=30, unique=True)     # 제조사명
    address = models.CharField(max_length=50, unique=True)  # 주소

    # 연락처
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)

    # 설립년도
    establishment = models.DateField()

    def __str__(self):  # 객체에 대한 문자열 리턴
        return self.name

    def get_absolute_url(self):
        return f'/shopping/maker/{self.pk}/'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)   # 카테고리는 unique해야 함
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)


    def __str__(self):  # 객체에 대한 문자열 리턴
        return self.name

    class Meta:   # verbose_name_plural은 예약어
        verbose_name_plural = 'Categories'   # admin페이지의 Categorys대신 들어감

    def get_absolute_url(self):
        return f'/shopping/category/{self.slug}/'

class Toy(models.Model):
    title = models.CharField(max_length=40)      # 상품명
    hook_text = models.CharField(max_length=100, blank=True)   # 미리보기 텍스트
    content = models.TextField()

    # 이미지 업로드
    head_image = models.ImageField(upload_to='shoppingmall/images/%Y/%m/%d/', blank=True)  # 이미지 저장 경로

    # 상품 가격
    price = models.IntegerField()

    # 제조사(다대일)
    maker = models.ForeignKey(Maker, null=True, on_delete=models.SET_NULL)

    # 카테고리(다대일)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # 재질 (다대다)
    material = models.ManyToManyField(Material, blank=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # 출시년도
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # 객체에 대한 문자열 리턴
        return self.title

    def get_absolute_url(self):
        return f'/shopping/{self.pk}/'       # 블로그 게시물의 url

    def get_avatar_url(self):

        # 소셜 로그인한 유저의 경우
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()        # 구글 아바타를 가져옴
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

# 댓글
class Comment(models.Model):
    # Post와 다대일 관계
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    댓글 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)        # 생성 시간은 자동으로 추가
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.댓글}'

    def get_absolute_url(self):
        return f'{self.toy.get_absolute_url()}#comment-{self.pk}'        # 상세 페이지 url

    def get_avatar_url(self):

        # 소셜 로그인한 유저의 경우
        if self.author.socialaccount_set.exists():
            if self.author.socialaccount_set.first().get_avatar_url() is not None:
                return self.author.socialaccount_set.first().get_avatar_url()       # 아바타를 가져옴
            else:
                return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'