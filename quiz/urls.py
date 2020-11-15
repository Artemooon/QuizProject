from django.urls import path

from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('',views.HomePage.as_view(),name = "home"),
    path('rating/',views.Rating.as_view(),name = "rating"),
    path('quiz/',views.QuizPage.as_view(),name = "quiz"),
    path('quiz/<slug:name>/<unique>/',views.game_view, name = "game_view"),
    path('quiz/<slug:name>/result/<slug:result>', views.QuizResult.as_view(), name = "quiz_result_url"),
    path('quiz/preview/<slug:name>',views.preview,name = "preview"),
    path('quiz/preview/<slug:name>/ajax',views.ajax_query, name = "ajax_query"),
    path('quiz/preview/<slug:name>/<int:id>/delete/',views.ajax_query_delete,name = 'ajax_query_delete',),
    path('quiz/preview/<slug:name>/<int:id>/edit/', views.ajax_query_edit, name = "ajax_query_edit"),
    path('quiz/preview/<slug:name>/like/', views.like_quiz, name = "likes_quiz"),
    path('quiz/preview/<slug:name>/dislike/', views.dislike_quiz, name = "dislikes_quiz"),
    path('quiz/preview/<slug:name>/like-comment/', views.like_comment, name = "likes_comment"),
    path('quiz/preview/<slug:name>/dislike-comment/', views.dislike_comment, name = "dislikes_comment"),
    path('quiz/<slug:name>/<unique>/t/',views.timer_ajax,name = "timer"),
    path('quiz-creation/',views.QuizCreation.as_view(),name = "quiz_creation"),
    path('quiz-creation/<slug:name>/',views.QuizQuestionsCreation.as_view(),name = "questions_creation")
]
