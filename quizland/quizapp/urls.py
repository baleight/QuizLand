"""
Configurazione degli URL per l'applicazione QuizLand.
Definisce tutti i percorsi URL disponibili nell'applicazione.
"""

from django.urls import path
from . import views

app_name = 'quizapp'

urlpatterns = [
    # URLs per la gestione base
    path('', views.home, name='home'),
    path('quiz/add/', views.add_quiz, name='add_quiz'),
    path('quiz/manage/', views.manage_quiz, name='manage_quiz'),
    
    # URLs per la gestione delle domande
    path('quiz/<int:quiz_pk>/questions/', views.manage_questions, name='manage_questions'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/edit/', views.edit_question, name='edit_question'),
    path('quiz/question/<int:question_pk>/delete/', views.delete_question, name='delete_question'),
    path('quiz/<int:quiz_pk>/question/add/', views.add_question, name='add_question'),
    
    # URLs per l'assegnazione e lo svolgimento dei quiz
    path('quiz/<int:quiz_type_id>/assign/', views.assign_quiz, name='assign_quiz'),
    path('quiz/<int:quiz_type_id>/take/', views.start_quiz, name='start_quiz'),
    # path('quiz/<int:quiz_type_id>/results/', views.QuizResultsView.as_view(), name='quiz_results'),
    
    # URLs per le contestazioni
    path('question/<int:question_pk>/dispute/', views.create_dispute, name='create_dispute'),
    path('disputes/', views.list_disputes, name='list_disputes'),
    path('dispute/<int:dispute_pk>/resolve/', views.resolve_dispute, name='resolve_dispute'),
    
    # URLs per le statistiche
    path('statistics/', views.quiz_statistics, name='quiz_statistics'),
    path('statistics/<int:quiz_type_id>/', views.quiz_statistics_detail, name='quiz_statistics_detail'),
    
    # URLs per gli studenti
    path('assignments/', views.student_assignments, name='student_assignments'),
    
    # URLs per la ripetizione dei quiz
    path('quiz/<int:quiz_type_id>/reset/', views.reset_quiz, name='reset_quiz'),
    
    # URLs per la cronologia dei quiz completati
    path('quiz/history/', views.quiz_history, name='quiz_history'),

    path('quiz/<int:assignment_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:assignment_id>/results/', views.quiz_results, name='quiz_results'),
]
