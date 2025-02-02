"""
Models per l'applicazione QuizLand.
Definisce la struttura del database e le relazioni tra le entità.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q  # Import necessario per le query condizionali
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

# Funzione per ottenere l'ID del primo superuser
def get_default_user():
    User = get_user_model()
    # Prova a ottenere il primo superuser, altrimenti il primo utente
    return User.objects.filter(is_superuser=True).first().id if User.objects.filter(is_superuser=True).exists() else User.objects.first().id

class Category(models.Model):
    """
    Modello per le categorie dei quiz.
    Permette di organizzare i quiz per argomento o materia.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class QuizType(models.Model):
    """
    Modello per i tipi di quiz.
    Rappresenta un quiz con le sue caratteristiche principali.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_quizzes',
        default=get_default_user  # Aggiunto default
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_total_questions(self):
        """Restituisce il numero totale di domande nel quiz"""
        return self.questions.count()

class Question(models.Model):
    """
    Modello per le domande dei quiz.
    Ogni domanda ha quattro opzioni e una risposta corretta.
    """
    ANSWER_CHOICES = [
        ('A', 'Opzione A'),
        ('B', 'Opzione B'),
        ('C', 'Opzione C'),
        ('D', 'Opzione D'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('EASY', 'Facile'),
        ('MEDIUM', 'Media'),
        ('HARD', 'Difficile'),
    ]

    quiz_type = models.ForeignKey(
        QuizType,
        on_delete=models.CASCADE,
        related_name='questions'  # Questo è il nome che stiamo usando
    )
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, default='MEDIUM')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quiz_type.name} - Domanda {self.id}"

class QuizSession(models.Model):
    """Modello per tracciare le sessioni di quiz degli utenti."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_type = models.ForeignKey(QuizType, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    date_taken = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.quiz_type.name} - Score: {self.score}"

    class Meta:
        ordering = ['-date_taken']

class QuizAssignment(models.Model):
    """
    Modello per le assegnazioni dei quiz.
    Tiene traccia di quali quiz sono stati assegnati a quali studenti.
    """
    quiz = models.ForeignKey(QuizType, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_assignments')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_quizzes')
    assigned_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    attempt_number = models.PositiveIntegerField(default=1)  # Aggiunto campo per il numero del tentativo

    class Meta:
        ordering = ['-assigned_date']

    def __str__(self):
        return f"{self.student.username} - {self.quiz.name} (Tentativo {self.attempt_number})"

    def is_overdue(self):
        """Verifica se il quiz è scaduto"""
        if self.due_date:
            return timezone.now() > self.due_date
        return False

class QuestionDispute(models.Model):
    """
    Modello per le contestazioni delle domande.
    Permette agli studenti di contestare domande specifiche.
    """
    STATUS_CHOICES = [
        ('OPEN', 'Aperta'),
        ('RESOLVED', 'Risolta'),
        ('REJECTED', 'Respinta'),
    ]

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disputes')
    reason = models.TextField(default='Contestazione precedente')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(default=timezone.now)
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='resolved_disputes'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_note = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Contestazione {self.id} - {self.student.username}"

    def resolve(self, resolver, status, note):
        """
        Risolve una contestazione
        
        Args:
            resolver: User che risolve la contestazione
            status: Nuovo stato della contestazione
            note: Nota di risoluzione
        """
        self.status = status
        self.resolved_by = resolver
        self.resolution_note = note
        self.resolved_at = timezone.now()
        self.save()

class QuizResponse(models.Model):
    assignment = models.ForeignKey(
        QuizAssignment,
        on_delete=models.CASCADE,
        related_name='quiz_responses'
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Verifica se la risposta è corretta prima di salvare
        self.is_correct = self.answer == self.question.correct_answer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Risposta {self.answer} alla domanda {self.question_id}"
