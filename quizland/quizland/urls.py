"""
Configurazione delle URL per il progetto QuizApp.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from quizapp import views

# Definizione delle rotte principali.
# Ogni path associa un URL a un modulo o applicazione specifica.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quizapp.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),
    path('register/', views.register, name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
