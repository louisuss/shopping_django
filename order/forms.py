from django import forms
from .models import Order


class RegisterForm(forms.Form):
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

        # 세션을 받아야하기 때문에 폼을 변경해야됨
