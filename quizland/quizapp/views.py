from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuizForm, QuestionForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, QuizSession, QuizType
from django.contrib.auth.decorators import user_passes_test


def home(request):
    quiz_types = QuizType.objects.all()
    return render(request, 'home.html', {'quiz_types': quiz_types})

def superuser_only(user):
    return user.is_superuser

@user_passes_test(superuser_only)
def manage_quiz(request):
    quizzes = QuizType.objects.all()
    return render(request, 'quiz/manage_quiz.html', {'quizzes': quizzes})

@user_passes_test(superuser_only)
def add_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz:manage-quiz')
    else:
        form = QuizForm()
    return render(request, 'quiz/add_quiz.html', {'form' : form})

@user_passes_test(superuser_only)
def update_quiz(request, pk):
    quiz = get_object_or_404(QuizType, pk=pk)
    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz:manage-quiz')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz/update_quiz.html', {'form':form, 'quiz':quiz})

@user_passes_test(superuser_only)
def delete_quiz(request, pk):
    quiz = get_object_or_404(QuizType, pk=pk)
    quiz.delete()
    return redirect('quiz:manage-quiz')

@user_passes_test(superuser_only)
def manage_questions(request, pk):
    quiz_type =  get_object_or_404(QuizType, pk=pk)
    questions = quiz_type.questions.all()
    return render(request, 'quiz/manage_questions.html', {'quiz_type':quiz_type, 'questions': questions})

@user_passes_test(superuser_only)
def add_questions(request, pk):
    quiz_type = get_object_or_404(QuizType, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz_type = quiz_type
            question.save()
            return redirect('quiz:manage_questions', pk=quiz_type.pk)
        else:
            print(form.errors)
    else:
        form = QuestionForm()

    # Adding Bootstrap classes
    for field in ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']:
        form.fields[field].widget.attrs.update({'class': 'form-control my-1'})

    return render(request, 'quiz/add_question.html', {'form': form, 'quiz_type': quiz_type})

@user_passes_test(superuser_only)
def update_question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('quiz:manage_questions', pk=question.quiz_type.pk)
    else:
        form = QuestionForm(instance=question)

    # Adding Bootstrap classes
    for field in ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']:
        form.fields[field].widget.attrs.update({'class': 'form-control my-1'})

    return render(request, 'quiz/update_question.html', {'form': form, 'question': question})

@user_passes_test(superuser_only)
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return redirect('quiz:manage_questions', pk=question.quiz_type.pk)


class InizioQuizView(LoginRequiredMixin, View):
    def get(self, request, quiz_type_id):
        try:
            quiz_type = QuizType.objects.get(id=quiz_type_id)
        except QuizType.DoesNotExist:
            return redirect('quiz:home')

        answered_questions = QuizSession.objects.filter(user=request.user).values_list('question_id', flat=True)

        remaining_questions = Question.objects.filter(quiz_type=quiz_type).exclude(id__in=answered_questions)

        if remaining_questions.exists():
            question = remaining_questions.order_by('?').first()
            question_index = answered_questions.count() + 1
            return render(request, 'quiz/start_quiz.html', {'question': question, 'quiz_type': quiz_type, 'question_index': question_index})
        else:
            return redirect('quiz:quiz_results', quiz_type_id=quiz_type_id)

class InviaAnswerView(LoginRequiredMixin, View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        quiz_type_id = question.quiz_type.id
        selected_answer = request.POST.get('answer')

        if not selected_answer:
            QuizSession.objects.create(user=request.user,
                                       question = question,
                                       status='unattempted'
                                       )
        else:
            is_correct = selected_answer == question.correct_answer
            QuizSession.objects.create(
                user=request.user,
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct,
                status = 'attempted'
            )

        answered_questions = QuizSession.objects.filter(user=request.user).values_list('question_id', flat=True)
        remaining_questions = Question.objects.filter(quiz_type=question.quiz_type).exclude(id__in=answered_questions)

        if remaining_questions.exists():
            return redirect('quiz:start_quiz', quiz_type_id=quiz_type_id)
        else:
            return redirect('quiz:quiz_results', quiz_type_id=quiz_type_id)


class RisultatiQuizView(LoginRequiredMixin, View):
    def get(self, request, quiz_type_id):

        quiz_type = get_object_or_404(QuizType, id=quiz_type_id)
        quiz_sessions = QuizSession.objects.filter(user=request.user, question__quiz_type=quiz_type)

        correct_answers = quiz_sessions.filter(is_correct=True).count()
        incorrect_answers = quiz_sessions.filter(is_correct=False).count()
        total_questions = quiz_sessions.count()
        unattempted_questions = QuizSession.objects.filter(user=request.user, status='unattempted').count()
        unattempted_session = quiz_sessions.filter(status='unattempted')
        return render(request, 'quiz/quiz_results.html', {
            'quiz_type': quiz_type,
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'total_questions': total_questions,
            'quiz_sessions': quiz_sessions,
            'unattempted_questions':  unattempted_questions,
            'unattempted_session' : unattempted_session,
        })


class ResetQuizView(LoginRequiredMixin, View):
    def get(self, request, pk):
        quiz_type = get_object_or_404(QuizType, id=pk)
        QuizSession.objects.filter(user=request.user, question__quiz_type=quiz_type).delete()
        return redirect('quiz:home')
