from django import forms
from .models import QuizType, Question

# Form per la gestione dei dati relativi ai quiz.
# Questo form consente di aggiungere e modificare i tipi di quiz.

class QuizForm(forms.ModelForm):
    class Meta:
        # Il modello associato a questo form è QuizType.
        model = QuizType

        # Campi del modello inclusi nel form.
        fields = ['name', 'description']

    def clean_name(self):
        # Metodo di validazione per il campo "name".
        # Controlla se esiste già un quiz con lo stesso nome (escludendo il quiz corrente in caso di modifica).
        name = self.cleaned_data.get('name')
        if QuizType.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A quiz with this name already exists.")
        return name

# Form per la gestione delle domande di un quiz.
# Questo form consente di aggiungere e modificare domande.

class QuestionForm(forms.ModelForm):
    class Meta:
        # Il modello associato a questo form è Question.
        model = Question

        # Campi del modello inclusi nel form.
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']

    def clean_question_text(self):
        # Metodo di validazione per il campo "question_text".
        # Controlla se esiste già una domanda con lo stesso testo (escludendo la domanda corrente in caso di modifica).
        question_text = self.cleaned_data.get('question_text')
        if Question.objects.filter(question_text=question_text).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Question already exists.")
        return question_text
