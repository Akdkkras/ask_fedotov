from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hot", views.index_hot, name="hot"),
    path("tag/<str:tag>", views.index_by_tag, name="tag"),
    path("question/<int:id>", views.question_page, name="question_page"),
    path("login", views.login_page, name="login_page"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_page, name="signup_page"),
    path("profile/edit", views.profile_edit, name="profile_edit"),
    path("ask", views.ask_page, name="ask_page"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
