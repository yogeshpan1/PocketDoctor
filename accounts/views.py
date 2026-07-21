from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SignUpForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        storage = messages.get_messages(self.request)
        for _ in storage:
            pass
        storage.used = True
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'doctor_profile') and user.doctor_profile is not None:
            return '/doctors/'
        return '/'


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')