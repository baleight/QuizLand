from django.db import models
from django.contrib.auth.models import User

# Modello per i tipi di quiz.
# Ogni tipo di quiz ha un nome univoco e una descrizione.
class QuizType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nome del quiz (deve essere univoco).
    description = models.TextField(blank=True)  # Descrizione del quiz.

    def __str__(self):
        # Rappresentazione leggibile del modello.
        return self.name

# Modello per le domande di un quiz.
# Ogni domanda appartiene a un tipo di quiz e ha un testo, quattro opzioni e una risposta corretta.
class Question(models.Model):
    quiz_type = models.ForeignKey(QuizType, related_name='questions', on_delete=models.CASCADE)  # Relazione con il modello QuizType.
    question_text = models.CharField(max_length=255)  # Testo della domanda.
    option_a = models.CharField(max_length=100)  # Opzione A.
    option_b = models.CharField(max_length=100)  # Opzione B.
    option_c = models.CharField(max_length=100)  # Opzione C.
    option_d = models.CharField(max_length=100)  # Opzione D.
    correct_answer = models.CharField(max_length=1)  # Lettera della risposta corretta (es. 'A').

    def __str__(self):
        # Rappresentazione leggibile del modello.
        return self.question_text

# Modello per le sessioni di quiz degli utenti.
# Tiene traccia delle risposte degli utenti e del loro stato.
class QuizSession(models.Model):
    STATUS_CHOICES = (
        ('attempted', 'Attempted'),  # Stato: tentato.
        ('unattempted', 'Unattempted'),  # Stato: non tentato.
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utente che ha partecipato al quiz.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Domanda a cui si riferisce la sessione.
    selected_answer = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])  # Risposta selezionata.
    is_correct = models.BooleanField(default=False)  # Indica se la risposta è corretta.
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='unattempted')  # Stato della domanda.

    def __str__(self):
        # Rappresentazione leggibile del modello.
        return f"{self.user.username} - {self.question.question_text}"
