from django import forms
from .models import QuizType, Question, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class QuizForm(forms.ModelForm):
    """
    Form per la gestione dei dati relativi ai tipi di quiz.
    Consente di aggiungere e modificare quiz, con validazioni personalizzate.
    """
    class Meta:
        model = QuizType
        fields = ['name', 'description', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Applica la classe CSS 'form-control' a tutti i campi
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        """
        Validazione del campo 'name'.
        Controlla se esiste già un quiz con lo stesso nome, escludendo il quiz corrente.
        """
        name = self.cleaned_data.get('name')
        if QuizType.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Esiste già un quiz con questo nome.")
        return name


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Inserisci il testo della domanda'
            }),
            'option_a': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opzione A'
            }),
            'option_b': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opzione B'
            }),
            'option_c': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opzione C'
            }),
            'option_d': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opzione D'
            }),
            'correct_answer': forms.Select(attrs={
                'class': 'form-control'
            }, choices=Question.ANSWER_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Applica la classe CSS a tutti i campi
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_question_text(self):
        question_text = self.cleaned_data.get('question_text')
        if Question.objects.filter(question_text=question_text).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("La domanda esiste già nel database.")
        return question_text

    def clean_correct_answer(self):
        answer = self.cleaned_data.get('correct_answer')
        if answer not in ['A', 'B', 'C', 'D']:
            raise forms.ValidationError('La risposta deve essere A, B, C o D')
        return answer


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Cognome',
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].label = 'Nome utente'
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = 'Password'
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].label = 'Conferma password'
