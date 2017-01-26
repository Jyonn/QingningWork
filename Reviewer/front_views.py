from django.shortcuts import render


def center(request):
    return render(request, "reviewer/center.html")


def rank(request):
    return render(request, "reviewer/rank.html")
