from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Avg, Count, Max, Q, F
from django.db.models.functions import Round
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import QuizType, Question, QuizAssignment, QuestionDispute, QuizResponse
from .forms import QuizForm, QuestionForm, CustomUserCreationForm
from django.contrib.auth.models import User

# Definizione della funzione is_teacher all'inizio del file
def is_teacher(user):
    """
    Verifica se un utente è un insegnante (staff)
    """
    return user.is_staff

def home(request):

    """
    Vista della homepage.
    Mostra contenuti diversi per professori, studenti e utenti anonimi.
    """
    if not request.user.is_authenticated:
        # Vista per utenti anonimi
        return render(request, 'quiz/home.html', {
            'is_anonymous': True
        })
    elif request.user.is_staff:
        # Vista per i professori
        quizzes = QuizType.objects.filter(created_by=request.user).annotate(
            total_assignments=Count('quizassignment'),
            completed_assignments=Count('quizassignment', filter=Q(quizassignment__completed=True)),
            average_score=Avg('quizassignment__score', filter=Q(quizassignment__completed=True))
        )
        
        open_disputes_count = QuestionDispute.objects.filter(status='OPEN').count()
        
        return render(request, 'quiz/home.html', {
            'is_teacher': True,
            'quizzes': quizzes,
            'open_disputes_count': open_disputes_count
        })
    else:
        # Vista per gli studenti
        # Ottieni tutti i quiz assegnati non completati
        pending_assignments = QuizAssignment.objects.filter(
            student=request.user,
            completed=False
        ).select_related('quiz').order_by('due_date')

        # Ottieni gli ultimi 5 quiz completati, ordinati per data di completamento
        completed_assignments = QuizAssignment.objects.filter(
            student=request.user,
            completed=True
        ).select_related('quiz').order_by('-completed_at')[:5]
        
        # Statistiche dello studente
        stats = {
            'total_completed': QuizAssignment.objects.filter(
                student=request.user, 
                completed=True
            ).count(),
            'avg_score': QuizAssignment.objects.filter(
                student=request.user,
                completed=True
            ).aggregate(Avg('score'))['score__avg'],
            'best_score': QuizAssignment.objects.filter(
                student=request.user,
                completed=True
            ).aggregate(Max('score'))['score__max']
        }
        
        return render(request, 'quiz/home.html', {
            'is_teacher': False,
            'pending_assignments': pending_assignments,
            'completed_assignments': completed_assignments,
            'stats': stats
        })

@login_required
@user_passes_test(is_teacher)
def add_quiz(request):
    """
    Vista per aggiungere un nuovo quiz.
    Solo per professori.
    """
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            messages.success(request, 'Quiz creato con successo!')
            return redirect('quizapp:manage_questions', quiz_pk=quiz.id)
    else:
        form = QuizForm()
    
    return render(request, 'quiz/add_quiz.html', {'form': form})

@login_required
@user_passes_test(is_teacher)
def manage_quiz(request):
    """
    Vista per gestire i quiz esistenti.
    Solo per professori.
    """
    quizzes = QuizType.objects.all().order_by('-created_at')
    return render(request, 'quiz/manage_quiz.html', {'quizzes': quizzes})

@login_required
@user_passes_test(is_teacher)
def edit_question(request, quiz_pk, question_pk):
    quiz = get_object_or_404(QuizType, pk=quiz_pk)
    question = get_object_or_404(Question, pk=question_pk, quiz_type=quiz)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Domanda modificata con successo!')
            return redirect('quizapp:manage_questions', quiz_pk=quiz_pk)
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'quiz/edit_question.html', {
        'form': form,
        'question': question,
        'quiz': quiz
    })

@login_required
@user_passes_test(is_teacher)
def manage_questions(request, quiz_pk):
    """
    Vista per gestire le domande di un quiz specifico.
    Solo per professori.
    """
    quiz = get_object_or_404(QuizType, pk=quiz_pk)
    questions = Question.objects.filter(quiz_type=quiz).order_by('created_at')
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz_type = quiz
            question.save()
            messages.success(request, 'Domanda aggiunta con successo!')
            return redirect('quizapp:manage_questions', quiz_pk=quiz_pk)
    else:
        form = QuestionForm()
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'form': form
    }
    
    return render(request, 'quiz/manage_questions.html', context)


@login_required
@user_passes_test(is_teacher)
def delete_question(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    quiz_pk = question.quiz_type.id
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Domanda eliminata con successo!')
        return redirect('quizapp:manage_questions', quiz_pk=quiz_pk)
    
    return redirect('quizapp:manage_questions', quiz_pk=quiz_pk) 
@login_required
@user_passes_test(is_teacher)
def add_question(request, quiz_pk):
    """
    Vista per aggiungere una nuova domanda a un quiz.
    Solo per professori.
    """
    quiz = get_object_or_404(QuizType, pk=quiz_pk)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz_type = quiz
            question.save()
            messages.success(request, 'Domanda aggiunta con successo!')
            return redirect('quizapp:manage_questions', quiz_pk=quiz_pk)
    else:
        form = QuestionForm()
    
    return render(request, 'quiz/add_question.html', {
        'quiz': quiz,
        'form': form
    })

@login_required
@user_passes_test(is_teacher)
def assign_quiz(request, quiz_type_id):
    """
    Vista per assegnare un quiz agli studenti.
    Solo per professori.
    """
    quiz = get_object_or_404(QuizType, pk=quiz_type_id)
    
    if request.method == 'POST':
        # Ottieni la lista degli studenti selezionati
        student_ids = request.POST.getlist('students')
        due_date_str = request.POST.get('due_date')
        
        # Converti la data di scadenza se fornita
        due_date = None
        if due_date_str:
            try:
                # Converti la data nel formato corretto per DateTime
                due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%d')
                # Imposta l'ora alla fine della giornata (23:59:59)
                due_date = due_date.replace(hour=23, minute=59, second=59)
                # Converti in timezone-aware datetime
                due_date = timezone.make_aware(due_date)
            except ValueError:
                messages.error(request, 'Formato data non valido.')
                return redirect('quizapp:assign_quiz', quiz_type_id=quiz_type_id)
        
        # Ottieni gli studenti (utenti non staff)
        students = User.objects.filter(id__in=student_ids, is_staff=False)
        
        # Crea le assegnazioni
        assignments_created = 0
        for student in students:
            # Verifica se esiste già un'assegnazione non completata
            existing_assignment = QuizAssignment.objects.filter(
                quiz=quiz,
                student=student,
                completed=False
            ).exists()
            
            if not existing_assignment:
                QuizAssignment.objects.create(
                    quiz=quiz,
                    student=student,
                    assigned_by=request.user,
                    due_date=due_date  # Ora può essere None o un datetime valido
                )
                assignments_created += 1
        
        if assignments_created > 0:
            messages.success(
                request, 
                f'Quiz assegnato con successo a {assignments_created} studenti!'
            )
        else:
            messages.warning(
                request, 
                'Nessuna nuova assegnazione creata. Gli studenti selezionati potrebbero già avere il quiz assegnato.'
            )
        return redirect('quizapp:manage_quiz')
    
    # Ottieni tutti gli studenti (utenti non staff)
    students = User.objects.filter(is_staff=False).order_by('username')
    
    # Ottieni le assegnazioni esistenti per questo quiz
    existing_assignments = QuizAssignment.objects.filter(
        quiz=quiz,
        completed=False
    ).values_list('student_id', flat=True)
    
    context = {
        'quiz': quiz,
        'students': students,
        'existing_assignments': existing_assignments
    }
    
    return render(request, 'quiz/assign_quiz.html', context)

@login_required
def start_quiz(request, quiz_type_id):
    """
    Vista per iniziare un quiz.
    Verifica che lo studente abbia l'assegnazione e non abbia già completato il quiz.
    """
    try:
        # Recupera il quiz e verifica l'assegnazione
        quiz = get_object_or_404(QuizType, pk=quiz_type_id)
        assignment = get_object_or_404(
            QuizAssignment,
            student=request.user,
            quiz=quiz,
            completed=False
        )
        
        # Verifica la scadenza del quiz
        if assignment.due_date and timezone.now().date() > assignment.due_date:
            messages.error(request, 'Questo quiz è scaduto.')
            return redirect('quizapp:home')
        
        # Verifica la presenza di domande
        questions = Question.objects.filter(quiz_type=quiz)
        if not questions.exists():
            messages.error(request, 'Questo quiz non contiene domande.')
            return redirect('quizapp:home')
        
        # Gestione della sottomissione del quiz
        if request.method == 'POST':
            score = 0
            total_questions = questions.count()
            
            # Usa una transazione per garantire l'integrità dei dati
            with transaction.atomic():
                # Calcola il punteggio
                for question in questions:
                    answer = request.POST.get(f'question_{question.id}')
                    if answer and answer == question.correct_answer:
                        score += 1
                
                # Calcola il punteggio in decimi
                final_score = round((score / total_questions) * 10, 2)
                
                # Aggiorna l'assignment
                assignment.score = final_score
                assignment.completed = True
                assignment.completed_at = timezone.now()
                assignment.save()
            
            messages.success(request, f'Quiz completato! Punteggio: {final_score}/10')
            return redirect('quizapp:quiz_results', quiz_type_id=quiz_type_id)
        
        # Renderizza il template per iniziare il quiz
        context = {
            'quiz': quiz,
            'questions': questions,
            'assignment': assignment
        }
        return render(request, 'quiz/take_quiz.html', context)
        
    except QuizAssignment.DoesNotExist:
        messages.error(request, 'Non hai accesso a questo quiz.')
        return redirect('quizapp:home')
    except Exception as e:
        messages.error(request, f'Si è verificato un errore: {str(e)}')
        return redirect('quizapp:home')

@login_required
def quiz_statistics_detail(request, quiz_type_id):
    """
    Vista per le statistiche dettagliate di un quiz specifico.
    """
    quiz = get_object_or_404(QuizType, pk=quiz_type_id)
    
    # Verifica i permessi
    if not request.user.is_staff and quiz.created_by != request.user:
        raise PermissionDenied
    
    # Statistiche generali
    stats = QuizAssignment.objects.filter(quiz=quiz).aggregate(
        total_attempts=Count('id'),
        completed_attempts=Count('id', filter=Q(completed=True)),
        avg_score=Round(Avg('score', filter=Q(completed=True)), 2),
        max_score=Max('score'),
    )
    
    # Distribuzione dei punteggi
    score_distribution = (
        QuizAssignment.objects
        .filter(quiz=quiz, completed=True)
        .values('score')
        .annotate(count=Count('id'))
        .order_by('score')
    )
    
    # Performance degli studenti
    student_performance = (
        QuizAssignment.objects
        .filter(quiz=quiz, completed=True)
        .select_related('student')
        .order_by('-score')
    )
    
    context = {
        'quiz': quiz,
        'stats': stats,
        'score_distribution': score_distribution,
        'student_performance': student_performance,
    }
    
    return render(request, 'quiz/statistics_detail.html', context)

@login_required
def quiz_results(request, assignment_id):
    """Vista per mostrare i risultati del quiz"""
    assignment = get_object_or_404(QuizAssignment, id=assignment_id)
    
    if assignment.student != request.user:
        return HttpResponseForbidden()
    
    # Recupera tutte le risposte dal database
    responses = QuizResponse.objects.filter(assignment=assignment)
    
    # Recupera le domande contestate
    disputed_questions = QuestionDispute.objects.filter(
        question__quiz_type=assignment.quiz,
        student=request.user
    ).values_list('question_id', flat=True)
    
    # Prepara i dati per il template
    questions = assignment.quiz.questions.all()
    student_answers = {r.question_id: r.answer for r in responses}
    correct_answers = {r.question_id for r in responses if r.is_correct}
    
    context = {
        'quiz': assignment.quiz,
        'assignment': assignment,
        'questions': questions,
        'answers': student_answers,
        'score': assignment.score,
        'total_questions': questions.count(),
        'correct_responses': len(correct_answers),
        'correct_answers': correct_answers,
        'disputed_questions': disputed_questions,
    }
    
    return render(request, 'quiz/quiz_results.html', context)

@login_required
def reset_quiz(request, quiz_type_id):
    """Vista per resettare un quiz e permettere un nuovo tentativo"""
    quiz = get_object_or_404(QuizType, pk=quiz_type_id)
    
    try:
        # Trova l'ultimo tentativo per questo quiz
        last_assignment = QuizAssignment.objects.filter(
            quiz=quiz,
            student=request.user
        ).order_by('-attempt_number').first()
        
        if not last_assignment:
            messages.error(request, 'Quiz non trovato.')
            return redirect('quizapp:home')
        
        # Verifica se c'è già un tentativo non completato
        existing_incomplete = QuizAssignment.objects.filter(
            quiz=quiz,
            student=request.user,
            completed=False
        ).exists()
        
        if existing_incomplete:
            messages.warning(request, 'Hai già un tentativo in corso per questo quiz.')
            return redirect('quizapp:home')
        
        # Crea una nuova assegnazione con attempt_number incrementato
        new_attempt_number = (last_assignment.attempt_number or 0) + 1
        
        new_assignment = QuizAssignment.objects.create(
            quiz=quiz,
            student=request.user,
            assigned_by=last_assignment.assigned_by,
            attempt_number=new_attempt_number
        )
        
        messages.success(request, f'Quiz resettato. Questo è il tuo tentativo #{new_attempt_number}.')
        return redirect('quizapp:take_quiz', assignment_id=new_assignment.id)
        
    except Exception as e:
        messages.error(request, f'Si è verificato un errore: {str(e)}')
        return redirect('quizapp:home')

@login_required
def create_dispute(request, question_pk):
    """Vista per creare una nuova contestazione"""
    question = get_object_or_404(Question, pk=question_pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            # Verifica se esiste già una contestazione aperta
            existing_dispute = QuestionDispute.objects.filter(
                question=question,
                student=request.user,
                status='OPEN'
            ).exists()
            
            if existing_dispute:
                messages.warning(request, 'Hai già una contestazione aperta per questa domanda.')
            else:
                QuestionDispute.objects.create(
                    question=question,
                    student=request.user,
                    reason=reason
                )
                messages.success(request, 'Contestazione inviata con successo.')
        else:
            messages.error(request, 'Devi fornire una motivazione per la contestazione.')
    
    # Redirect alla pagina dei risultati
    assignment = QuizAssignment.objects.filter(
        student=request.user,
        quiz=question.quiz_type,
        completed=True
    ).latest('completed_at')
    
    return redirect('quizapp:quiz_results', assignment_id=assignment.id)

@login_required
def list_disputes(request):
    """
    Vista per visualizzare le contestazioni.
    Per i professori: tutte le contestazioni
    Per gli studenti: solo le proprie contestazioni
    """
    if request.user.is_staff:
        open_disputes = QuestionDispute.objects.filter(status='OPEN')
        resolved_disputes = QuestionDispute.objects.filter(status='RESOLVED')
        rejected_disputes = QuestionDispute.objects.filter(status='REJECTED')
        
        context = {
            'open_disputes': open_disputes,
            'resolved_disputes': resolved_disputes,
            'rejected_disputes': rejected_disputes,
            'is_teacher': True
        }
    else:
        disputes = QuestionDispute.objects.filter(student=request.user)
        context = {
            'disputes': disputes,
            'is_teacher': False
        }
    
    return render(request, 'quiz/list_disputes.html', context)

@login_required
@user_passes_test(is_teacher)
def resolve_dispute(request, dispute_pk):
    dispute = get_object_or_404(QuestionDispute, pk=dispute_pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        resolution_note = request.POST.get('resolution_note')
        
        if status in ['RESOLVED', 'REJECTED'] and resolution_note:
            dispute.status = status
            dispute.resolution_note = resolution_note
            dispute.resolved_by = request.user
            dispute.resolved_at = timezone.now()
            dispute.save()
            messages.success(request, 'Contestazione aggiornata con successo.')
            return redirect('quizapp:list_disputes')
        else:
            messages.error(request, 'Devi specificare sia lo stato che una nota di risoluzione.')
    
    return render(request, 'quiz/resolve_dispute.html', {
        'dispute': dispute
    })

@login_required
def student_assignments(request):
    """
    Vista per mostrare le assegnazioni degli studenti.
    """
    if request.user.is_staff:
        # Vista professore: tutte le assegnazioni
        assignments = QuizAssignment.objects.all().select_related(
            'student', 'quiz'
        ).order_by('-assigned_date')
    else:
        # Vista studente: solo le proprie assegnazioni
        assignments = QuizAssignment.objects.filter(
            student=request.user
        ).select_related('quiz').order_by('-assigned_date')
    
    return render(request, 'quiz/student_assignments.html', {
        'assignments': assignments,
        'is_teacher': request.user.is_staff
    })

@login_required
def quiz_statistics(request):
    """
    Vista per le statistiche generali dei quiz.
    """
    if not request.user.is_staff:
        raise PermissionDenied
    
    quizzes = QuizType.objects.annotate(
        total_attempts=Count('quizassignment'),
        completed_attempts=Count('quizassignment', filter=Q(quizassignment__completed=True)),
        avg_score=Round(Avg('quizassignment__score', filter=Q(quizassignment__completed=True)), 2)
    )
    
    return render(request, 'quiz/statistics.html', {
        'quizzes': quizzes
    })

@login_required
def quiz_history(request):
    """Vista per mostrare la cronologia dei quiz completati"""
    # Recupera tutti i quiz completati dall'utente, ordinati per data
    completed_assignments = QuizAssignment.objects.filter(
        student=request.user,
        completed=True
    ).select_related('quiz').order_by('-completed_at')
    
    context = {
        'quiz_history': completed_assignments,  # Passa direttamente gli assignment
    }
    
    return render(request, 'quiz/quiz_history.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account creato con successo! Ora puoi effettuare il login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def quiz_detail(request, assignment_id):
    """Vista dettaglio quiz per gli studenti"""
    # Recupera l'assignment o restituisce 404
    assignment = get_object_or_404(QuizAssignment, id=assignment_id)
    
    # Verifica che lo studente sia autorizzato
    if assignment.student != request.user:
        return HttpResponseForbidden("Non sei autorizzato a vedere questo quiz")
    
    # Prepara il contesto
    context = {
        'assignment': assignment,
        'quiz': assignment.quiz,
        'questions': assignment.quiz.questions.all()
    }
    
    return render(request, 'quiz/quiz_detail.html', context)

@login_required
def submit_quiz(request, assignment_id):
    """Vista per il submit del quiz"""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    assignment = get_object_or_404(QuizAssignment, id=assignment_id)
    
    if assignment.student != request.user:
        return HttpResponseForbidden()
    
    # Debug: stampa i dati ricevuti
    print("DEBUG - Dati POST ricevuti:", request.POST)
    
    # Elimina eventuali risposte precedenti
    QuizResponse.objects.filter(assignment=assignment).delete()
    
    # Contatore per le risposte corrette
    correct_count = 0
    total_questions = assignment.quiz.questions.count()
    
    # Salva le risposte
    for question in assignment.quiz.questions.all():
        answer_key = f'question_{question.id}'
        answer = request.POST.get(answer_key)
        
        print(f"Processing question {question.id}: answer={answer}, correct={question.correct_answer}")
        
        if answer:
            is_correct = (answer == question.correct_answer)
            response = QuizResponse.objects.create(
                assignment=assignment,
                question=question,
                answer=answer,
                is_correct=is_correct
            )
            print(f"Created response: {response.id} - Answer: {response.answer}")
            if is_correct:
                correct_count += 1
    
    # Calcola e salva il punteggio
    score = round((correct_count / total_questions) * 10, 2) if total_questions > 0 else 0
    
    # Aggiorna l'assignment
    assignment.score = score
    assignment.completed = True
    assignment.completed_at = timezone.now()
    assignment.save()
    
    print(f"Quiz completed - Score: {score}, Correct: {correct_count}/{total_questions}")
    
    # Verifica finale delle risposte salvate
    saved_responses = QuizResponse.objects.filter(assignment=assignment)
    print("Saved responses:", [(r.question_id, r.answer) for r in saved_responses])
    
    return redirect('quizapp:quiz_results', assignment_id=assignment.id)

@login_required
def take_quiz(request, assignment_id):
    assignment = get_object_or_404(QuizAssignment, id=assignment_id)
    
    if request.method == 'POST':
        print("\n=== DEBUG SUBMIT QUIZ ===")
        print("POST data:", dict(request.POST))
        print("Assignment ID:", assignment_id)
        
        # Elimina eventuali risposte precedenti
        QuizResponse.objects.filter(assignment=assignment).delete()
        
        correct_count = 0
        total_questions = assignment.quiz.questions.count()
        responses_created = []
        
        # Salva le risposte
        for question in assignment.quiz.questions.all():
            answer_key = f'question_{question.id}'
            answer = request.POST.get(answer_key)
            print(f"\nProcessing question {question.id}:")
            print(f"Answer key: {answer_key}")
            print(f"Answer value: {answer}")
            print(f"Correct answer: {question.correct_answer}")
            
            if answer:
                is_correct = (answer == question.correct_answer)
                try:
                    response = QuizResponse.objects.create(
                        assignment=assignment,
                        question=question,
                        answer=answer,
                        is_correct=is_correct
                    )
                    if is_correct:
                        correct_count += 1
                    responses_created.append(response)
                    print(f"Created response: {response.id}, answer={response.answer}, correct={response.is_correct}")
                except Exception as e:
                    print(f"Error saving response: {str(e)}")
        
        # Calcola e salva il punteggio
        score = round((correct_count / total_questions) * 10, 2) if total_questions > 0 else 0
        
        print(f"\nFinal calculation:")
        print(f"Correct answers: {correct_count}")
        print(f"Total questions: {total_questions}")
        print(f"Score: {score}")
        
        # Aggiorna l'assignment
        assignment.score = score
        assignment.completed = True
        assignment.completed_at = timezone.now()
        assignment.save()
        
        # Verifica finale
        saved_responses = QuizResponse.objects.filter(assignment=assignment)
        print("\nAll saved responses:")
        for resp in saved_responses:
            print(f"Question {resp.question_id}: Answer={resp.answer}, Correct={resp.is_correct}")
        
        return redirect('quizapp:quiz_results', assignment_id=assignment.id)
    
    context = {
        'quiz': assignment.quiz,
        'assignment': assignment,
        'questions': assignment.quiz.questions.all()
    }
    return render(request, 'quiz/take_quiz.html', context)