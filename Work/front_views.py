from django.shortcuts import render


def detail(request, wid):
    return render(request, "work/detail.html")


def upload(request):
    return render(request, "work/upload.html")
