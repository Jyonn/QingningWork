from django.shortcuts import render


def center(request):
    return render(request, "reviewer/center.html")


def rank(request, rank_type):
    return render(request, "reviewer/rank.html")
