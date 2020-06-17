from django import forms
from .models import Order
from product.models import Product
from user.models import User
from django.db import transaction


class RegisterForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ProductDetail View에서 request 받음
        self.request = request

    quantity = forms.IntegerField(
        error_messages={
            'required': '수량을 입력해주세요.'
        },
        label='수량'
    )
    product = forms.IntegerField(
        error_messages={
            'required': '상품설명을 입력해주세요.'
        },
        label='상품', widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        # product_detail -> value 값으로 id 받음
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')

        # 세션을 받아야하기 때문에 폼을 변경해야됨 __init__ 생성
        user = self.request.session.get('user')

        if quantity and product and user:
            with transaction.atomic():
                prod = Product.objects.get(pk=product)
                order = Order(
                    quantity=quantity,
                    product=prod,
                    user=User.objects.get(email=user)
                )
                order.save()
                prod.stock -= quantity
                prod.save()
        else:
            # 실패하면 메시지를 보여주고 싶은데 어떤 페이지에 보여줄지 모름. 그래서 form_invalid 시 redirect 해야함
            self.product = product
            self.add_error('quantity', '값이 없습니다.')
            self.add_error('product', '값이 없습니다.')
