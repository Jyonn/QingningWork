from django.shortcuts import render


def center(request):
    return render(request, "writer/center.html")
