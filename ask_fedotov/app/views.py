from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike


def paginate(objects, request: HttpRequest, per_page=10):
    page_num = request.GET.get("page", 1)
    paginator = Paginator(objects, per_page)
    try:
        page = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)

    return page


def index(request: HttpRequest):
    # questions = Question.qs.order_by_new() # 33 sql-запроса
    questions = Question.qs.order_by_new().prefetch_related( # 6 sql-запросов
        "tags",
        "answers",
        "likes",
    )
    page_obj = paginate(questions, request, 10)
    tags = Tag.objects.all()
    return render(request, "index.html", context={"tags_pool": tags, "page_obj": page_obj})
    # return render(request, "test.html")


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
        context={"tags_pool": tags, "page_obj": page_obj, "question": question}
    )


def login_page(request: HttpRequest):
    tags = Tag.objects.all()
    return render(request, "login.html", context={"tags_pool": tags})


def signup_page(request: HttpRequest):
    tags = Tag.objects.all()
    return render(request, "signup.html", context={"tags_pool": tags})


def settings_page(request: HttpRequest):
    tags = Tag.objects.all()
    return render(request, "settings.html", context={"tags_pool": tags})


def ask_page(request: HttpRequest):
    tags = Tag.objects.all()
    return render(request, "ask.html", context={"tags_pool": tags})