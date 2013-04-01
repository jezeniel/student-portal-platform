from django.shortcuts import render, redirect

from .forms import LectureForm


def create_lecture(request):
    form = LectureForm()
    return render(request, "development/form_sample.html", {'lecture_form': form})

