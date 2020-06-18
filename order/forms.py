from django import forms
from .models import Order
from product.models import Product
from user.models import User


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
            'required': '상품명을 입력해주세요.'
        },
        label='상품', widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        # product_detail -> value 값으로 id 받음
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')

        if not (quantity and product):
            self.add_error('quantity', '값이 없습니다.')
            self.add_error('product', '값이 없습니다.')
