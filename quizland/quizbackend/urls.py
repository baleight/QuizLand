"""
Configurazione delle URL per il progetto QuizApp.
"""

from django.contrib import admin
from django.urls import path, include

# Definizione delle rotte principali.
# Ogni path associa un URL a un modulo o applicazione specifica.
urlpatterns = [
    path("admin/", admin.site.urls),  # Accesso al pannello di amministrazione.
    path("", include("quiz.urls")),  # Rotte per l'applicazione "quiz".
    path("", include("users.urls")),  # Rotte per l'applicazione "users".
]
