from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import QuizType, Question, QuizAssignment, Category

class QuizLandTests(TestCase):
    def setUp(self):
        """Setup iniziale per tutti i test"""
        # Crea utenti test
        self.teacher = User.objects.create_user(
            username='prof1',
            password='test123',
            is_staff=True
        )
        self.student = User.objects.create_user(
            username='student1',
            password='test123'
        )
        self.student = User.objects.create_user(
            username='student2',
            password='test123'
        )
        
        
        # Crea quiz di test
        self.category = Category.objects.create(name='Test Category')
        self.quiz = QuizType.objects.create(
            name='Test Quiz',
            description='Quiz di test',
            category=self.category,
            created_by=self.teacher
        )
        
        # Crea domande test
        self.question1 = Question.objects.create(
            quiz_type=self.quiz,
            question_text='Domanda 1',
            option_a='A',
            option_b='B',
            option_c='C',
            option_d='D',
            correct_answer='A'
        )
        self.question2 = Question.objects.create(
            quiz_type=self.quiz,
            question_text='Domanda 2',
            option_a='A',
            option_b='B',
            option_c='C',
            option_d='D',
            correct_answer='B'
        )
        
        # Crea assignment
        self.assignment = QuizAssignment.objects.create(
            quiz=self.quiz,
            student=self.student,
            assigned_by=self.teacher
        )
        
        # Setup client
        self.client = Client()

    def test_quiz_assignment(self):
        """Test dell'assegnazione e completamento del quiz"""
        # Verifica creazione corretta dell'assignment
        self.assertEqual(self.assignment.quiz, self.quiz)
        self.assertEqual(self.assignment.student, self.student)
        self.assertEqual(self.assignment.assigned_by, self.teacher)
        self.assertFalse(self.assignment.completed)
        
        # Simula completamento quiz
        self.assignment.completed = True
        self.assignment.score = 7.5
        self.assignment.save()
        
        # Verifica completamento
        self.assertTrue(self.assignment.completed)
        self.assertEqual(self.assignment.score, 7.5)

    def test_quiz_view(self):
        """Test della vista del quiz"""
        # Login come studente
        self.client.login(username='student1', password='test123')
        
        # Test accesso alla pagina del quiz
        response = self.client.get(
            reverse('quizapp:quiz_detail', args=[self.assignment.id])
        )
        self.assertEqual(response.status_code, 200)
        
        # Verifica che le domande siano presenti nel contesto
        self.assertIn('questions', response.context)
        questions = response.context['questions']
        self.assertEqual(questions.count(), 2)
        
        # Verifica il contenuto della pagina
        self.assertContains(response, 'Domanda 1')
        self.assertContains(response, 'Domanda 2')
        
        # Test accesso non autorizzato
        self.client.logout()
        response = self.client.get(
            reverse('quizapp:quiz_detail', args=[self.assignment.id])
        )
        self.assertEqual(response.status_code, 302)  # Redirect al login
        
        # Test accesso come altro studente
        other_student = User.objects.create_user(
            username='student2',
            password='test123'
        )
        self.client.login(username='student2', password='test123')
        response = self.client.get(
            reverse('quizapp:quiz_detail', args=[self.assignment.id])
        )
        self.assertEqual(response.status_code, 403)  # Forbidden