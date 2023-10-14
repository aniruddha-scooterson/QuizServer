from django.urls import path

from . import views

urlpatterns = [
    path('api/v1/register', views.index, name='register'),
    path('', views.home_page, name='home'),
    path('api/v1/get_quiz_category', views.CategoryViewSet.as_view({'get': 'list'}), name='quiz_category'),
    path('api/v1/get_leaderboard', views.QuizUserScoreViewSet.as_view({'get': 'list'}), name='leadership_board'),
    path('api/v1/user_score/<int:pk>', views.QuizUserScoreIndividualViewSet.as_view({'get': 'retrieve'}), name='user_score'),
    path('api/v1/quiz_submit', views.QuizAnswerViewSet.as_view({'post': 'create'}), name='quiz'),
]

