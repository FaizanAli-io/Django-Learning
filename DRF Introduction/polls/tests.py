import datetime

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question('past', days=-30)
        create_choice(question, 'choice 1')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        question = create_question('future', days=30)
        create_choice(question, 'choice 1')
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_and_future_questions(self):
        question1 = create_question('past', days=-30)
        create_choice(question1, 'choice 1')
        question2 = create_question('future', days=30)
        create_choice(question2, 'choice 1')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question1],
        )

    def test_two_past_questions(self):
        question1 = create_question('past1', days=-30)
        create_choice(question1, 'choice 1')
        question2 = create_question('past2', days=-5)
        create_choice(question2, 'choice 1')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

    def test_choiceless_question(self):
        create_question('no choice', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_question_with_single_choice(self):
        question = create_question('question', days=-5)
        create_choice(question, 'choice 1')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_question_with_and_without_choice(self):
        question1 = create_question('question 1', days=-10)
        create_choice(question1, 'choice 1')
        create_question('question 2', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question1],
        )

    def test_question_with_multiple_choices(self):
        question = create_question('question', days=-5)
        create_choice(question, 'choice 1')
        create_choice(question, 'choice 2')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )


class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        question = create_question('past', days=-30)
        create_choice(question, 'choice 1')
        url = reverse('polls:detail', args=(question.id, ))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)

    def test_future_question(self):
        question = create_question('future', days=30)
        create_choice(question, 'choice 1')
        url = reverse('polls:detail', args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_choiceless_question(self):
        question = create_question('no choice', days=-5)
        url = reverse('polls:detail', args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_question_with_single_choice(self):
        question = create_question('question', days=-5)
        create_choice(question, 'choice 1')
        url = reverse('polls:detail', args=(question.id, ))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)


class QuestionResultsViewTests(TestCase):
    def test_past_question(self):
        question = create_question('past', days=-30)
        create_choice(question, 'choice 1')
        url = reverse('polls:results', args=(question.id, ))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)

    def test_future_question(self):
        question = create_question('future', days=30)
        create_choice(question, 'choice 1')
        url = reverse('polls:results', args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_choiceless_question(self):
        question = create_question('no choice', days=-5)
        url = reverse('polls:results', args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_question_with_single_choice(self):
        question = create_question('question', days=-5)
        create_choice(question, 'choice 1')
        url = reverse('polls:results', args=(question.id, ))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)


def create_question(question_text, **kwargs):
    time = timezone.now() + datetime.timedelta(**kwargs)
    return Question.objects.create(
        question_text=question_text,
        pub_date=time,
    )


def create_choice(question, choice_text):
    return question.choice_set.create(
        choice_text=choice_text,
    )
