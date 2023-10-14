from django.contrib.auth.models import User
from django.db import models

# Create your models here.

QUESTION_TYPE = (
    ('MCQ', 'Multiple Choice Question'),
    ('TF', 'True or False')
)
OPTIONS = (
    (1, 'option1/True'), (2, 'option2/False'), (3, 'option3'), (4, 'option4')
)


class Category(models.Model):
    category_name = models.CharField(max_length=30, verbose_name='category_name')

    def __str__(self):
        return f"Category: {self.id} {self.category_name}"


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=30, verbose_name='quiz_name')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='category_id', null=True)
    is_anonymous = models.BooleanField(verbose_name='is_anonymous', default=False)
    is_active = models.BooleanField(verbose_name='is_active', default=True)

    def __str__(self):
        return f"Quiz: {self.id} {self.quiz_name}"


class QuestionAnswerOptionType(models.Model):
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPE, verbose_name='question_answer_option_type')
    option1 = models.CharField(max_length=100, verbose_name='option1')
    option2 = models.CharField(max_length=100, verbose_name='option2')
    option3 = models.CharField(max_length=100, verbose_name='option3', blank=True, null=True)
    option4 = models.CharField(max_length=100, verbose_name='option4', blank=True, null=True)
    correct_option = models.IntegerField(verbose_name='correct_option')

    def __str__(self):
        return f"Option Type: {self.question_type} , {self.option1}, {self.option2}, {self.option3}, {self.option4}"


class QuestionBank(models.Model):
    question_description = models.CharField(max_length=200, verbose_name="question_description")
    answer_option_type_id = models.ForeignKey(QuestionAnswerOptionType, on_delete=models.SET_NULL, null=True)
    points = models.IntegerField(verbose_name='points')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Question: {self.id}, {self.question_description}"


class QuizQuestions(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    question_id = models.ForeignKey(QuestionBank, on_delete=models.SET_NULL, null=True)
    active_question_in_quiz = models.BooleanField(verbose_name='active_question', default=True)

    def __str__(self):
        return f"Quiz Question id: : {self.id}, Question id: : {self.question_id_id}, Quiz: {self.quiz_id}"


class QuizUserScoreSheet(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    quiz_questions = models.ForeignKey(QuizQuestions, on_delete=models.SET_NULL, null=True)
    option_selected = models.IntegerField(choices=OPTIONS, verbose_name='option_selected')
    score = models.IntegerField(verbose_name='score')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Score Sheet {self.id}, User id: {self.user_id_id}"


class QuizUserScore(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    user_score = models.IntegerField(verbose_name='user_score')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"User score: {self.user_id} Quiz: {self.quiz_id}"