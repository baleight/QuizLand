from django.contrib import admin
from .models import Category, Question, QuizSession, QuizType, QuizAssignment, QuestionDispute


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz_type', 'difficulty', 'correct_answer']  # Mostra questi campi nella lista
    list_filter = ['quiz_type', 'difficulty']  # Filtra per questi campi
    search_fields = ['question_text']  # Permette la ricerca per testo della domanda
    ordering = ('quiz_type', 'created_at')


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz_type', 'score', 'date_taken')
    list_filter = ('quiz_type', 'user')
    search_fields = ('user__username',)


@admin.register(QuizType)  # Usando il decoratore per registrare il modello
class QuizTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_by', 'created_at']
    list_filter = ['category', 'created_by']
    search_fields = ['name', 'description']
    ordering = ('-created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(QuizAssignment)
class QuizAssignmentAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'student', 'assigned_by', 'assigned_date', 'completed', 'score')
    list_filter = ('completed', 'quiz', 'assigned_by')
    search_fields = ('student__username', 'quiz__name')
    ordering = ('-assigned_date',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se è una nuova assegnazione
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(QuestionDispute)
class QuestionDisputeAdmin(admin.ModelAdmin):
    list_display = ('question', 'student', 'status', 'created_at', 'resolved_by')
    list_filter = ('status', 'created_at')
    search_fields = ('question__question_text', 'student__username')
    ordering = ('-created_at',)
