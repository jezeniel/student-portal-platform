from xml.etree import ElementTree
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Subject, SubjectInvitation
from .forms import AddSubjectForm
from bbb.models import Meeting
from announcement.forms import SubjectAnnouncementForm
from announcement.models import SubjectAnnouncement
from lecture.forms import LectureUploadForm
from lecture.models import LectureFile
from quiz.forms import QuizUploadForm
from quiz.models import Quiz, Question, Choice

@login_required
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


@login_required
def course_view(request, course_id):
    subject = get_object_or_404(Subject, id=course_id)
    meeting = get_object_or_404(Meeting, subject=subject)
    lectures = subject.lecturefile_set.all()
    studentgroup = Group.objects.get(name='student').user_set.all()
    students = []
    for student in studentgroup:
        info = "%s" % (student.email)
        students.append(str(info))

    if request.user.groups.all()[0].name == 'teacher':
        template = "final/course-view-teacher.html"
    else:
        template = "final/course-view-student.html"

    if request.method == "GET":
        announcement_form = SubjectAnnouncementForm()
        lecture_upload_form = LectureUploadForm()
        quiz_upload_form = QuizUploadForm()


    elif request.method == "POST":
        announcement_form = SubjectAnnouncementForm(request.POST)
        if announcement_form.is_valid():
            SubjectAnnouncement.objects.create(subject=subject, author=request.user,
                                   title=announcement_form.cleaned_data['title'],
                                   content=announcement_form.cleaned_data['content'])
            return redirect(subject.get_absolute_url())

    return render(request, template, {'subject': subject, 'all_students': students,
                                      'announcementform': announcement_form, "quizuploadform": quiz_upload_form,
                                      'lectureuploadform': lecture_upload_form, 'lectures': lectures})


@login_required
def lecture_upload(request, course_id):
    subject = get_object_or_404(Subject, id=course_id)
    if request.method == "POST":
        uploadform = LectureUploadForm(request.POST, request.FILES)
        if uploadform.is_valid():
            lec_file = LectureFile(subject=subject, docfile=request.FILES['docfile'])
            lec_file.save()
            messages.success(request, "Successfully uploaded the file.")
        else:
            messages.error(request, "Failed to upload the file.")
    return redirect(subject.get_absolute_url())

@login_required
def lecture_delete(request, lecture_id):
    lecture = get_object_or_404(LectureFile, id=lecture_id)
    subject = lecture.subject
    lecture.delete()
    messages.success(request, "Successfully deleted the file.")
    return redirect(subject.get_absolute_url())

@login_required
def quiz_upload(request, course_id):
    subject = get_object_or_404(Subject, id=course_id)
    if request.method == "POST":
        uploadform = QuizUploadForm(request.POST, request.FILES)
        if uploadform.is_valid():
            xmlfile = request.FILES.get('xmlfile')
            tree = ElementTree.XML(xmlfile.read())
            quiz = Quiz.objects.create(subject=subject, title=tree.attrib['name'])
            for qstion in tree:
                question = Question.objects.create(quiz=quiz, question=qstion.attrib['text'])
                for choice in qstion:
                    if choice.attrib.get('correct', False):
                        is_correct = True
                    else:
                        is_correct = False
                    Choice.objects.create(question=question, choice_text=choice.text, is_correct=is_correct)
    return redirect(subject.get_absolute_url())

@login_required
def add_student(request, course_id):
    subject = Subject.objects.get(id=course_id)
    if request.method == "POST":
        email = request.POST.get("student-email")
        if email:
            student = User.objects.get(email=email)
            obj, created = SubjectInvitation.objects.get_or_create(teacher=request.user, student=student, subject=subject)
            if created:
                msg = "Successfully sent course invitation to %s." % (email)
                messages.success(request, msg)
            else:
                messages.error(request, "You already sent an invitation to this user.")
        else:
            messages.error(request, "Invalid email address!")
    return redirect(subject.get_absolute_url())

@login_required
def accept_course_invite(request, course_id):
    subject = get_object_or_404(Subject, id=course_id)
    invitation = request.user.course_invitations.get(subject=subject)
    invitation.accept()
    messages.success(request, "You successfully joined the subject.")
    return redirect(subject.get_absolute_url())

@login_required
def decline_course_invite(request, course_id):
    subject = get_object_or_404(Subject, id=course_id)
    invitation = request.user.course_invitations.get(subject=subject)
    invitation.decline()
    return redirect("home_url")
