from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_field_name='next'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/quiz/'
    ), name='logout'),
] 