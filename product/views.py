from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from rest_framework import generics, mixins

from user.decorators import admin_required
from .models import Product
from .forms import RegisterForm
from .serializers import ProductSerializer
from order.forms import RegisterForm as OrderForm

# Create your views here.


class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    # 어떤 데이터를 가지고 REST API를 명시할지 정해야함
    # 데이터 검증
    serializer_class = ProductSerializer

    # 가져올 데이터 명시
    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        # mixins 클래스에서 list 함수 사용하여 model로 부터 데이터를 가져와 JSON 형태로 바꿔줌
        return self.list(request, *args, **kwargs)

# RetrieveModelMixin : 상세보기를 위한 mixins


class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    # get -> url에서 pk 값을 연결해줘야됨. 앞의 queryset에서 특정값만 빼서씀.
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'


@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stock=form.data.get('stock')
        )
        product.save()
        return super().form_valid(form)


class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = OrderForm(self.request)

        return context
