from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse

from .models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from .forms import SignUpForm, LoginForm, AskForm, ProfileEditForm, AnswerForm
from .utils import parse_tags


def paginate(objects, request: HttpRequest, per_page=10):
    page_num = request.GET.get("page", 1)
    paginator = Paginator(objects, per_page)
    try:
        page = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)

    return page


def index(request: HttpRequest):
    questions = Question.qs.order_by_new().prefetch_related(
        "tags",
        "answers",
        "likes",
    )
    page_obj = paginate(questions, request, 10)
    tags = Tag.objects.all()
    return render(request, "index.html", context={"tags_pool": tags, "page_obj": page_obj})


def index_hot(request: HttpRequest):
    questions = Question.qs.order_by_likes().prefetch_related(
        "tags",
        "answers",
        "likes",
    )
    page_obj = paginate(questions, request, 10)
    tags = Tag.objects.all()
    return render(request, "index_hot.html", context={"tags_pool": tags, "page_obj": page_obj})


def index_by_tag(request: HttpRequest, tag):
    questions = Question.qs.order_by_new().filter(tags__name=tag).prefetch_related(
        "tags",
        "answers",
        "likes",
    )
    page_obj = paginate(questions, request, 10)
    tags = Tag.objects.all()
    return render(request, "index_by_tag.html", context={"tags_pool": tags, "page_obj": page_obj})


def question_page(request: HttpRequest, id):
    if request.method == "POST":
        user = request.user
        profile = get_object_or_404(Profile, user=user)

        form = AnswerForm(request.POST)
        if form.is_valid():
            Question.objects.get(pk=id).answers.create(
                user=profile,
                text=form.cleaned_data["text"]
            )
            return HttpResponseRedirect(reverse("question_page", kwargs={"id": id}))
    else:
        form = AnswerForm()

    question = Question.objects.prefetch_related(
        "tags",
        "answers",
        "likes",
    ).get(pk=id)
    answers = question.answers.all().prefetch_related(
        "likes",
    )
    page_obj = paginate(answers, request, 5)

    tags = Tag.objects.all()
    return render(
        request,
        "question.html",
        context={"tags_pool": tags, "page_obj": page_obj,
                 "question": question, "form": form}
    )


def login_page(request: HttpRequest):
    next_url = request.GET.get("continue")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse("index"))
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    tags = Tag.objects.all()
    return render(request, "login.html", context={"tags_pool": tags, "form": form})


def logout_view(request: HttpRequest):
    if request.method == "POST":
        logout(request)
        next_url = request.POST.get("next")
        if next_url:
            return HttpResponseRedirect(next_url)
    return HttpResponseRedirect(reverse("index"))


@transaction.atomic
def signup_page(request: HttpRequest):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            Profile.objects.create(
                user=user,
                nickname=form.cleaned_data["nickname"],
                avatar=form.cleaned_data.get("avatar")
            )

            return HttpResponseRedirect(reverse("index"))
    else:
        form = SignUpForm()

    tags = Tag.objects.all()
    return render(request, "signup.html", context={"tags_pool": tags, "form": form})


@login_required
def profile_edit(request: HttpRequest):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, user=user)

        if form.is_valid():
            user.username = form.cleaned_data["username"]
            user.email = form.cleaned_data["email"]

            profile.nickname = form.cleaned_data["nickname"]
            if form.cleaned_data["avatar"]:
                profile.avatar = form.cleaned_data["avatar"]

            user.save()
            profile.save()
            return HttpResponseRedirect(reverse('profile_edit'))
    else:
        form = ProfileEditForm(initial={
            "username": user.username,
            "email": user.email,
            "nickname": profile.nickname,
        }, user=user)

    tags = Tag.objects.all()
    return render(request, "profile_edit.html", context={"tags_pool": tags, "form": form})


@login_required
def ask_page(request: HttpRequest):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, user=request.user)
            tags = parse_tags(form.cleaned_data["tags"])

            question = Question.objects.create(
                user=profile,
                title=form.cleaned_data["title"],
                text=form.cleaned_data["text"],
            )
            question.tags.set(tags)

            return HttpResponseRedirect(reverse("question_page", kwargs={"id": question.id}))
    else:
        form = AskForm()

    tags = Tag.objects.all()
    return render(request, "ask.html", context={"tags_pool": tags, "form": form})
