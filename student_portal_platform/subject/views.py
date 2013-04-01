from django.shortcuts import render, redirect, get_object_or_404

from .models import Subject
from .forms import AddSubjectForm
from bbb.models import Meeting


def course_list(request):
    if request.method == "GET":
        addform = AddSubjectForm()
    elif request.method == "POST":
        addform = AddSubjectForm(request.POST)
        if addform.is_valid():
            Subject.objects.create(name=addform.cleaned_data['name'],
                                   teacher=request.user,
                                   start_date=addform.cleaned_data['start_date'],
                                   end_date=addform.cleaned_data['end_date'],
                                   private=addform.cleaned_data['private'])
            return redirect("course:list")

    return render(request, "final/course.html", {'addsubjectform': addform})


def course_view(request, course_id):
    subject = get_object_or_404(Subject, id=course_id)
    meeting = Meeting.objects.get(subject=subject)
    return render(request, "final/course-view.html", {'subject': subject})
