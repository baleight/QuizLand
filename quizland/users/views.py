from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import  login
from .forms import RegistrationForm, CustomAuthenticationForm
from django.contrib.auth import authenticate
# Create your views here.

class UserRegistrationView(SuccessMessageMixin, FormView):
    template_name = 'registration/registration.html' 
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')  
    success_message = "Registration Successful! You can log in."

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm
    success_url = '/'
    
    def form_valid(self, form):
        user  = authenticate(
            username = form.cleaned_data.get('username'),
            password = form.cleaned_data.get('password'),
        )
        if user:
            login(self.request, user)
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        return form