from django.shortcuts import render


def center(request):
    return render(request, "v2/center.html")


def login_v2(request):
    return render(request, "v2/login.html")


def login(request):
    return render(request, "login.html")


def info(request):
    return render(request, "info.html")
