from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


question_list = [{
    "id": i,
    "title": f"title{i}",
    "text": f"text{i}",
} for i in range(33)]


def index(request: HttpRequest):
    return render(request, "index.html", context={"questions": question_list})

def index_hot(request: HttpRequest):
    return render(request, "index_hot.html")