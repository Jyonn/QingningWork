from django.shortcuts import render


def user(request):
    return render(request, 'v2/comment-list.html')


def work(request):
    return render(request, "v2/work.html")


def center(request):
    return render(request, "v2/center.html")


def login_v2(request):
    return render(request, "v2/login.html")


def login(request):
    return render(request, "login.html")


def info(request):
    return render(request, "info.html")
