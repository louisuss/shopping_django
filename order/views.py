from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from user.decorators import login_required
from .forms import RegisterForm
from .models import Order
from user.models import User
from product.models import Product

from django.db import transaction

# Create your views here.


@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        with transaction.atomic():
            prod = Product.objects.get(pk=form.data.get('product'))
            order = Order(
                quantity=form.data.get('quantity'),
                product=prod,
                user=User.objects.get(email=self.request.session.get('user'))
            )
            order.save()
            prod.stock -= int(form.data.get('quantity'))
            prod.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('/product/' + str(form.data.get('product')))

    # 이 FormView 에서도 request 를 받은것을 입력해줘야됨
    def get_form_kwargs(self, **kwargs):
        # FormView가 알아서 생성하는 인자값들을 만듬
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        # 기존에 생성되는 인자값에 request도 함께 생성해서 전달
        return kw


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    # 다른사람이 주문한 정보도 볼수 있게 됨. 때문에 직접 queryset을 만듬. -> 세션이 필요. 사용자 정보가 필요하기 때문
    # model = Order
    template_name = 'order.html'
    context_object_name = 'order_list'

    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(
            user__email=self.request.session.get('user'))
        return queryset

    # method_decorator를 사용안할경우 다음과 같은 함수를 호출해줘야함
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)
