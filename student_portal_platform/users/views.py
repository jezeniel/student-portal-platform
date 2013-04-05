import os
from datetime import date, datetime
from PIL import Image

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail

from .models import UserInfo, ForgotPassword
from .forms import AccountForm, PersonalForm, ProfileEdit, AccountEdit, ForgetPasswordForm, ForgetNewPasswordForm


def register(request):
    if request.method.upper() == 'GET':
        if not request.user.is_authenticated():
            return render(request, 'official/form.html', {'accountform': AccountForm(),
                                                          'personalform': PersonalForm()})
        return redirect("home_url")

    elif request.method.upper() == 'POST':
        form = AccountForm(request.POST)
        form2 = PersonalForm(request.POST)
        if form.is_valid() and form2.is_valid():
            userdata = {key: value for (key, value) in form.cleaned_data.items()}
            userdata2 = {key: value for (key, value) in form2.cleaned_data.items()}
            user = User.objects.create_user(username=userdata['username'],
                                            password=userdata['password1'],
                                            email=userdata['email'],
                                            first_name=userdata2['firstname'],
                                            last_name=userdata2['lastname'])

            userinfo = UserInfo.objects.create(user=user,
                                               address=userdata2['address'],
                                               gender=userdata2['gender']
                                               )

            g = Group.objects.get(name='student')
            g.user_set.add(user)
            messages.info(request, "Registered successfully.")
            return redirect("login_url")

        else:
            return render(request, 'official/form.html', {'accountform': form, 'personalform': form2})


@login_required
def editaccount(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "GET":
        editaccount_form = AccountEdit(initial={'email': user.email})
    elif request.method == "POST":
        editaccount_form = AccountEdit(user=request.user, data=request.POST)
        if editaccount_form.is_valid():
            old_email = user.email
            user.email = editaccount_form.cleaned_data['email']
            newpassword = editaccount_form.cleaned_data.get("password1")
            change = False
            if old_email != user.email:
                messages.success(request, "You successfully chaged your email address.")
                change = True
            if newpassword:
                user.set_password(newpassword)
                messages.success(request, "You successfully changed your password.")
                change = True
            if change:
                user.save()
            return redirect('editaccount')
    return render(request, "final/editaccount.html", {'editaccount_form': editaccount_form})


@login_required
def editprofile(request):
    user = User.objects.get(id=request.user.id)
    userinfo = user.userinfo
    print userinfo.primaryphoto
    if request.method == "GET":
        pf = ProfileEdit(initial={'primaryphoto': userinfo.primaryphoto,
                                  'firstname': user.first_name, 'lastname': user.last_name,
                                  'address': userinfo.address, 'gender': userinfo.gender,
                                  'course': userinfo.course, 'birthday': userinfo.birthday,
                                  'about_me': userinfo.about_me})
    elif request.method == "POST":
        pf = ProfileEdit(request.POST, request.FILES)
        print request.FILES
        if pf.is_valid():
            userdata = {key: value for (key, value) in pf.cleaned_data.items()}
            if request.FILES.get('primaryphoto', None):
                userinfo.primaryphoto = request.FILES.get('primaryphoto', None)
                userinfo.save()
                image_handler(userinfo.primaryphoto.path)
            user.first_name = userdata['firstname']
            user.last_name = userdata['lastname']
            userinfo.address = userdata['address']
            userinfo.gender = userdata['gender']
            userinfo.course = userdata['course']
            userinfo.birthday = userdata['birthday']
            userinfo.about_me = userdata['about_me']
            user.save()
            userinfo.save()
            return redirect("editprofile")
    return render(request, "final/editprofile.html", {'pf': pf})


def forget_password(request):
    if request.user.is_authenticated():
        return redirect('home_url')
    elif request.method == "GET":
        forget_form = ForgetPasswordForm()

    elif request.method == "POST":
        forget_form = ForgetPasswordForm(request.POST)
        if forget_form.is_valid():
            obj, created = ForgotPassword.objects.get_or_create(email=forget_form.cleaned_data['email'])
            if not created:
                obj.email = forget_form.cleaned_data['email']
                obj.save()

            #send password reset in email
            print obj.code
            msg = "visit this link to change your pass /newpassword/%s" % (obj.code)
            send_mail('E-learning Portal Reset Password', msg, 'Online Social Learning System',[obj.email])

            messages.success(request, "Successfully sent password reset link.")
            return redirect("login_url")
    return render(request, "official/forget-password.html", {'forget_form': forget_form})


def forget_new_password(request, code):
    forgot = get_object_or_404(ForgotPassword, code=code)
    if request.method == "GET":
        if not request.user.is_authenticated():
            new_password_form = ForgetNewPasswordForm()
            return render(request, "official/forget-new-password.html", {'newpassword_form': new_password_form})
    elif request.method == "POST":
        new_password_form = ForgetNewPasswordForm(request.POST)
        if new_password_form.is_valid():
            user = User.objects.get(email=forgot.email)
            user.set_password(new_password_form.cleaned_data['password1'])
            forgot.delete()
            user.save()
            messages.success(request, "Successfully changed your password.")
        else:
            return render(request, "official/forget-new-password.html", {'newpassword_form': new_password_form})
    return redirect('login_url')



def image_handler(imagename):
    file_name, file_ext = os.path.splitext(imagename)
    im = Image.open(imagename)
    if file_ext.lower() in [".png", ".gif"]:
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, im)
    else:
        bg = im
    thumb_sizes = [(128,128), (64, 64), (32, 32)]
    for thumb_size in thumb_sizes:
        thumb_name = "thumb_%s" % (thumb_size[0])
        imgname = file_name + thumb_name + file_ext
        image_resize(bg, thumb_size, imgname)


def image_resize(image, size, imagename):
    image = image.resize(size, Image.ANTIALIAS)
    image.save(imagename, "JPEG")
