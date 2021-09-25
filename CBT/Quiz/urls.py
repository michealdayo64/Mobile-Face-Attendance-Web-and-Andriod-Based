from django.urls import path
from .views import (quizListView, quizDetailView, quiz_data_view, save_quiz_view)

app_name = 'Quiz'

urlpatterns = [
    path('', quizListView, name = 'quiz_list'),
    path('<pk>/', quizDetailView, name = 'quiz_detail'),
    path('<pk>/data/', quiz_data_view, name = 'quiz_data'),
    path('<pk>/save/', save_quiz_view, name = 'quiz_save')
]

