import random
import random
import string

from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

random.seed(1)

tags_pool = ["python", "golang", "java", "c++", "sql", "ai", "django", "react", "linux", "docker"]

QUESTIONS_LIST_SIZE = 92
ANSWERS_LIST_SIZE = 60

questions_list = [{
    "id": i,
    "title": f"title{i}",
    "text": ''.join(random.choices(string.ascii_lowercase + 10 * ' ', k=random.randint(50, 300))),
    "tags": sorted(random.sample(tags_pool, k=random.randint(1, len(tags_pool)))),
    "answers_number": random.randint(0, ANSWERS_LIST_SIZE - 1),
    "likes_number": random.randint(0, 100),
} for i in range(QUESTIONS_LIST_SIZE)]

answers_list = [{
    "user_id": i,
    "text": ''.join(random.choices(string.ascii_lowercase + 10 * ' ', k=random.randint(50, 300))),
    "is_verified": random.choice([True, False]),
    "likes_number": random.randint(0, 100),
}for i in range(ANSWERS_LIST_SIZE)]


def paginate(objects_list, request : HttpRequest, per_page=10):
    page_num = request.GET.get("page", 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(1)

    return page


def index(request: HttpRequest):
    page_obj = paginate(questions_list, request, 10)
    return render(request, "index.html", context={"page_obj": page_obj, "tags_pool": tags_pool})

def index_hot(request: HttpRequest):
    sorted_questions = sorted(questions_list, key=lambda x: x['likes_number'], reverse=True)
    page_obj = paginate(sorted_questions, request, 10)
    return render(request, "index_hot.html", context={"page_obj": page_obj, "tags_pool": tags_pool})

def index_by_tag(request: HttpRequest, tag):
    filtered_questions = [q for q in questions_list if tag in q["tags"]]
    page_obj = paginate(filtered_questions, request, 10)
    return render(request,"index_by_tag.html", context={"page_obj": page_obj, "tags_pool": tags_pool, "current_tag": tag})

def question_page(request: HttpRequest, id):
    question = next((q for q in questions_list if q["id"] == id), None)
    answers_number = question["answers_number"]
    page_obj = paginate(answers_list[:answers_number], request, 5)
    return render(request, "question.html", context={"page_obj": page_obj, "question": question, "tags_pool": tags_pool})

def login_page(request: HttpRequest):
    return render(request, "login.html", context={"tags_pool": tags_pool})

def signup_page(request: HttpRequest):
    return render(request, "signup.html", context={"tags_pool": tags_pool})

def settings_page(request: HttpRequest):
    return render(request, "settings.html", context={"tags_pool": tags_pool})

def ask_page(request: HttpRequest):
    return render(request, "ask.html", context={"tags_pool": tags_pool})
