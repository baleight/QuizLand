from django.apps import AppConfig

# Configurazione dell'applicazione Django per la gestione dei quiz.
# Questa configurazione definisce il comportamento dell'app all'interno del progetto.

class QuizappConfig(AppConfig):
    # Definizione del tipo di chiave primaria predefinita per i modelli.
    default_auto_field = "django.db.models.BigAutoField"

    # Nome dell'applicazione, che deve corrispondere al nome della directory contenente questa configurazione.
    name = "quizapp"
