from django.shortcuts import render


def center(request):
    return render(request, "writer/center.html")


def rank(request, rank_type):
    return render(request, "writer/rank.html")
