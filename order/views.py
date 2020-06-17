from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm
# Create your views here.


class OrderCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_invalid(self, form):
        return redirect('/product/' + str(form.product))

    # 이 FormView 에서도 request 를 받은것을 입력해줘야됨
    def get_form_kwargs(self, **kwargs):
        # FormView가 알아서 생성하는 인자값들을 만듬
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        # 기존에 생성되는 인자값에 request도 함께 생성해서 전달
        return kw
