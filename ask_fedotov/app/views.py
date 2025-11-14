from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike


# tags_pool = [tag.name for tag in Tag.objects.all()]

# questions = Question.objects.all().prefetch_related('tags', 'answers', 'likes')
# answers = Answer.objects.all().select_related('user').prefetch_related('likes')

# questions_list = [
#     {
#         "id": q.id,
#         "title": q.title,
#         "text": q.text,
#         "tags": list(q.tags.values_list('name', flat=True)),
#         "answers_number": q.answers.count(),
#         "likes_number": q.likes.count(),
#     }
#     for q in questions
# ]

# answers_list = [
#     {
#         "user_id": answer.user.id,
#         "text": answer.text,
#         "is_verified": True,
#         "likes_number": answer.likes.count(),
#     }
#     for answer in answers
# ]


def get_tags_pool():
    return list(Tag.objects.all().values_list("name", flat=True))

def get_questions_list():
    questions = Question.objects.all().prefetch_related('tags', 'answers', 'likes')

    return [
        {
            "id": q.id,
            "title": q.title,
            "text": q.text,
            "tags": list(q.tags.values_list('name', flat=True)),
            "answers_number": q.answers.count(),
            "likes_number": q.likes.count(),
        }
        for q in questions
    ]

def get_answers_list():
    answers = Answer.objects.all().select_related('user').prefetch_related('likes')

    return [
        {
            "user_id": answer.user.id,
            "text": answer.text,
            "is_verified": True,
            "likes_number": answer.likes.count(),
        }
        for answer in answers
    ]

def paginate(objects_list, request: HttpRequest, per_page=10):
    page_num = request.GET.get("page", 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)

    return page


def index(request: HttpRequest):
    tags_pool = get_tags_pool()
    questions_list = get_questions_list()
    page_obj = paginate(questions_list, request, 10)
    return render(request, "index.html", context={"page_obj": page_obj, "tags_pool": tags_pool})

def index_hot(request: HttpRequest):
    tags_pool = get_tags_pool()
    questions_list = get_questions_list()
    sorted_questions = sorted(questions_list, key=lambda x: x['likes_number'], reverse=True)
    page_obj = paginate(sorted_questions, request, 10)
    return render(request, "index_hot.html", context={"page_obj": page_obj, "tags_pool": tags_pool})


def index_by_tag(request: HttpRequest, tag):
    tags_pool = get_tags_pool()
    questions_list = get_questions_list()
    filtered_questions = [q for q in questions_list if tag in q["tags"]]
    page_obj = paginate(filtered_questions, request, 10)
    return render(
        request,
        "index_by_tag.html",
        context={"page_obj": page_obj, "tags_pool": tags_pool, "current_tag": tag},
    )


def question_page(request: HttpRequest, id):
    tags_pool = get_tags_pool()
    questions_list = get_questions_list()
    answers_list = get_answers_list()

    question = next((q for q in questions_list if q["id"] == id), None)
    answers_number = question["answers_number"]
    page_obj = paginate(answers_list[:answers_number], request, 5)

    return render(
        request,
        "question.html",
        context={"page_obj": page_obj, "question": question, "tags_pool": tags_pool},
    )


def login_page(request: HttpRequest):
    return render(request, "login.html", context={"tags_pool": get_tags_pool()})


def signup_page(request: HttpRequest):
    return render(request, "signup.html", context={"tags_pool": get_tags_pool()})


def settings_page(request: HttpRequest):
    return render(request, "settings.html", context={"tags_pool": get_tags_pool()})


def ask_page(request: HttpRequest):
    return render(request, "ask.html", context={"tags_pool": get_tags_pool()})