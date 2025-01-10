from django.urls import path
from . import views

# Definizione dello spazio dei nomi per le URL dell'applicazione.
# Questo consente di distinguere le rotte di questa app da quelle di altre app nel progetto.
app_name = 'quizapp'

# Definizione delle rotte URL per l'app Quiz.
urlpatterns = [
    path('', views.home, name='home'),  # Homepage dell'app.
    path('start/<int:quiz_type_id>/', views.InizioQuizView.as_view(), name='start_quiz'),  # Inizio di un quiz.
    path('submit_answer/<int:question_id>/', views.InviaAnswerView.as_view(), name='submit_answer'),  # Invio di una risposta.
    path('results/<int:quiz_type_id>/', views.RisultatiQuizView.as_view(), name='quiz_results'),  # Visualizzazione dei risultati.
    path('reset/<int:pk>/', views.ResetQuizView.as_view(), name='reset_quiz'),  # Reset di un quiz.
    path('manage-quiz/', views.manage_quiz, name="manage-quiz"),  # Gestione dei quiz per gli amministratori.
    path('add-quiz/', views.add_quiz, name="add_quiz"),  # Aggiunta di un nuovo quiz.
    path('update-quiz/<int:pk>/', views.update_quiz, name="update_quiz"),  # Modifica di un quiz esistente.
    path('delete-quiz/<int:pk>/', views.delete_quiz, name="delete_quiz"),  # Eliminazione di un quiz.
    path('add-question/<int:pk>/', views.add_questions, name='add_question'),  # Aggiunta di una domanda a un quiz.
    path('update-question/<int:pk>/', views.update_question, name="update_question"),  # Modifica di una domanda.
    path('delete-question/<int:pk>/', views.delete_question, name='delete_question'),  # Eliminazione di una domanda.
    path('questions/manage/<int:pk>/', views.manage_questions, name='manage_questions'),  # Gestione delle domande.
]
