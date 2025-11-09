from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hot", views.index_hot, name="hot"),
    path("tag/<str:tag>", views.index_by_tag, name="tag"),
    path("question/<int:id>", views.question_page, name="question_page"),
    path("login", views.login_page, name="login_page"),
    path("signup", views.signup_page, name="signup_page"),
    path("settings", views.settings_page, name="settings_page"),
    path("ask", views.ask_page, name="ask_page"),
]
