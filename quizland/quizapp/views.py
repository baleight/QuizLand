from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuizForm, QuestionForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, QuizSession, QuizType
from django.contrib.auth.decorators import user_passes_test

# Funzione per visualizzare la homepage.
# Recupera tutti i tipi di quiz dal database e li passa al template "home.html".
def home(request):
    quiz_types = QuizType.objects.all()  # Recupera tutti i tipi di quiz.
    return render(request, 'home.html', {'quiz_types': quiz_types})  # Renderizza la homepage con i quiz disponibili.

# Funzione di controllo per verificare se l'utente è un superuser.
# Questa funzione è utilizzata come decoratore per limitare l'accesso alle funzioni di gestione dei quiz.
def superuser_only(user):
    return user.is_superuser  # Ritorna True solo se l'utente è un amministratore.

# Funzione per la gestione dei quiz da parte degli amministratori.
# Recupera tutti i quiz esistenti e li passa al template "manage_quiz.html".
@user_passes_test(superuser_only)
def manage_quiz(request):
    quizzes = QuizType.objects.all()  # Recupera tutti i quiz dal database.
    return render(request, 'quiz/manage_quiz.html', {'quizzes': quizzes})  # Renderizza la pagina di gestione dei quiz.

# Funzione per aggiungere un nuovo quiz.
# Se il metodo della richiesta è POST, salva il nuovo quiz, altrimenti mostra il form vuoto.
@user_passes_test(superuser_only)
def add_quiz(request):
    if request.method == "POST":  # Controlla se il metodo della richiesta è POST.
        form = QuizForm(request.POST)  # Inizializza il form con i dati inviati dall'utente.
        if form.is_valid():  # Controlla se i dati del form sono validi.
            form.save()  # Salva il nuovo quiz nel database.
            return redirect('quiz:manage-quiz')  # Reindirizza alla pagina di gestione dei quiz.
    else:
        form = QuizForm()  # Inizializza un form vuoto per la creazione di un nuovo quiz.
    return render(request, 'quiz/add_quiz.html', {'form': form})  # Renderizza la pagina di aggiunta quiz.

# Funzione per modificare un quiz esistente.
@user_passes_test(superuser_only)
def update_quiz(request, pk):
    quiz = get_object_or_404(QuizType, pk=pk)  # Recupera il quiz o restituisce un errore 404.
    if request.method == "POST":  # Controlla se il metodo della richiesta è POST.
        form = QuizForm(request.POST, instance=quiz)  # Inizializza il form con i dati esistenti.
        if form.is_valid():  # Controlla se i dati del form sono validi.
            form.save()  # Salva le modifiche nel database.
            return redirect('quiz:manage-quiz')  # Reindirizza alla pagina di gestione dei quiz.
    else:
        form = QuizForm(instance=quiz)  # Inizializza un form con i dati del quiz da modificare.
    return render(request, 'quiz/update_quiz.html', {'form': form, 'quiz': quiz})  # Renderizza la pagina di modifica quiz.

# Funzione per eliminare un quiz.
@user_passes_test(superuser_only)
def delete_quiz(request, pk):
    quiz = get_object_or_404(QuizType, pk=pk)  # Recupera il quiz o restituisce un errore 404.
    quiz.delete()  # Elimina il quiz dal database.
    return redirect('quiz:manage-quiz')  # Reindirizza alla pagina di gestione dei quiz.

# Funzione per gestire le domande associate a un quiz.
@user_passes_test(superuser_only)
def manage_questions(request, pk):
    quiz_type = get_object_or_404(QuizType, pk=pk)  # Recupera il tipo di quiz.
    questions = quiz_type.questions.all()  # Recupera tutte le domande associate al quiz.
    return render(request, 'quiz/manage_questions.html', {'quiz_type': quiz_type, 'questions': questions})  # Renderizza la pagina di gestione delle domande.

# Funzione per aggiungere domande a un quiz.
@user_passes_test(superuser_only)
def add_questions(request, pk):
    quiz_type = get_object_or_404(QuizType, pk=pk)  # Recupera il tipo di quiz.
    if request.method == "POST":  # Controlla se il metodo della richiesta è POST.
        form = QuestionForm(request.POST)  # Inizializza il form con i dati inviati dall'utente.
        if form.is_valid():  # Controlla se i dati del form sono validi.
            question = form.save(commit=False)  # Crea un'istanza della domanda senza salvarla.
            question.quiz_type = quiz_type  # Associa la domanda al quiz.
            question.save()  # Salva la domanda nel database.
            return redirect('quiz:manage_questions', pk=quiz_type.pk)  # Reindirizza alla gestione delle domande.
    else:
        form = QuestionForm()  # Inizializza un form vuoto per la creazione di una nuova domanda.

    # Aggiunge classi Bootstrap ai campi del form per migliorare lo stile.
    for field in ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']:
        form.fields[field].widget.attrs.update({'class': 'form-control my-1'})

    return render(request, 'quiz/add_question.html', {'form': form, 'quiz_type': quiz_type})  # Renderizza la pagina di aggiunta domande.
