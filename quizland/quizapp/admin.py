from django.contrib import admin
from .models import Question, QuizSession, QuizType

# Registrazione dei modelli al pannello di amministrazione di Django.
# Questo permette agli amministratori di gestire i dati direttamente dal pannello admin.

# Il modello Question rappresenta le domande associate ai quiz.
admin.site.register(Question)

# Il modello QuizSession tiene traccia delle risposte degli utenti durante un quiz.
admin.site.register(QuizSession)

# Il modello QuizType definisce i tipi di quiz disponibili nell'applicazione.
admin.site.register(QuizType)
