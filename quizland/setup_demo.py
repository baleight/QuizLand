# Creiamo uno script setup_demo.py nella root del progetto
from django.contrib.auth.models import User
from quizapp.models import Category, QuizType, Question, QuizAssignment

def setup_demo_data():
    # Crea utenti di test
    try:
        # Crea un insegnante
        teacher1 = User.objects.create_user(
            username='teacher1',
            password='teacher1password',
            email='teacher1@example.com',
            is_staff=True
        )
        
        # Crea uno studente
        student1 = User.objects.create_user(
            username='student1',
            password='student1password',
            email='student1@example.com'
        )
        
        # Crea categorie
        category1 = Category.objects.create(
            name='Programmazione',
            description='Quiz sulla programmazione'
        )
        
        category2 = Category.objects.create(
            name='Database',
            description='Quiz sui database'
        )
        
        # Crea quiz
        quiz1 = QuizType.objects.create(
            name='Python Base',
            description='Quiz sui concetti base di Python',
            category=category1,
            created_by=teacher1
        )
        
        # Crea domande per il quiz
        Question.objects.create(
            quiz_type=quiz1,
            question_text='Qual è il tipo di dato di "Hello World"?',
            option_a='str',
            option_b='int',
            option_c='float',
            option_d='bool',
            correct_answer='A',
            difficulty='EASY'
        )
        
        Question.objects.create(
            quiz_type=quiz1,
            question_text='Come si crea una lista vuota in Python?',
            option_a='list()',
            option_b='[]',
            option_c='Entrambe A e B',
            option_d='{}',
            correct_answer='C',
            difficulty='MEDIUM'
        )
        
        print("Dati demo creati con successo!")
        
    except Exception as e:
        print(f"Errore durante la creazione dei dati demo: {str(e)}")
