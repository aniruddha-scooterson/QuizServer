from django.contrib import admin
from QZ_Star.models import Category
from QZ_Star.models import QuestionAnswerOptionType
from QZ_Star.models import QuestionBank
from QZ_Star.models import Quiz
from QZ_Star.models import QuizQuestions
from QZ_Star.models import QuizUserScore
from QZ_Star.models import QuizUserScoreSheet


# Register your models here.

admin.site.register(Category)
admin.site.register(QuestionAnswerOptionType)
admin.site.register(QuestionBank)
admin.site.register(Quiz)
admin.site.register(QuizQuestions)
admin.site.register(QuizUserScore)
admin.site.register(QuizUserScoreSheet)
