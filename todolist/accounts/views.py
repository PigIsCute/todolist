from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse

# Create your views here.
class UserRegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('task-list')

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('task-list')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')