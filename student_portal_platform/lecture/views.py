from django.shortcuts import render, redirect

from .forms import LectureForm

def create_lecture(request):
    form = LectureForm()
    return render(request, "final/lecture-add.html", {'lecture_form': form})

