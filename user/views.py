from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
# Create your views here.


def index(request):
    return render(request, 'index.html', {'email': request.session.get('user')})


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    # 로그인이 정상적으로 됐을 때 들어오는 함수
    def form_valid(self, form):
        self.request.session['user'] = form.email
        return super().form_valid(form)
