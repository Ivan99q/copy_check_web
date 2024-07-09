from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from werkzeug.utils import secure_filename
import os

UPLOAD_PATH = os.path.join(os.path.dirname(__file__), "tmp_files")


def index(request):
    return render(request, "index.html")


@csrf_exempt
def upload_file(request):

    if request.method == "POST" and request.FILES["file"]:
        uploaded_file = request.FILES["file"]
        file_content = uploaded_file.read().decode("utf-8")

        # 处理文件内容，这里可以根据需要做进一步的处理
        duprate = check(file_content)
        # 返回JSON响应，包括上传成功和文件内容
        return JsonResponse({"success": True, "content": duprate})
    else:
        return JsonResponse({"success": False})


def check(file_content):
    # 进行查重，返回查重率

    return 0.5


def result_page(request):
    return render(request, "result.html")
