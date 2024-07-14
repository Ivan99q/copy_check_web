from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from werkzeug.utils import secure_filename
import os


def index(request):
    return render(request, "index.html")


@csrf_exempt
def submit(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        author = request.POST.get("author", "")
        content = request.POST.get("content", "")
        return render(
            request,
            "result.html",
            {"title": title, "author": author, "content": content},
        )
    else:
        return HttpResponse("Method not allowed", status=405)


def shash(content: str):
    # TODO 计算simhash
    return 1515165153123123


def result_page(request):
    return render(request, "result.html")
