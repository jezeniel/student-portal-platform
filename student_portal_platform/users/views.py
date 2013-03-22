import os
from datetime import date, datetime
from PIL import Image

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import UserInfo
from .forms import AccountForm, PersonalForm, ProfileEdit


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

            messages.info(request, "Registered successfully.")
            return redirect("login_url")

        else:
            return render(request, 'official/form.html', {'accountform': form, 'personalform': form2})


def editaccount(request):
    user = User.objects.get(id=request.user.id)


def editprofile(request):
    user = User.objects.get(id=request.user.id)
    userinfo = user.userinfo
    if request.method == "GET":
        pf = ProfileEdit(initial={'firstname': user.first_name, 'lastname': user.last_name,
                                  'address': userinfo.address, 'gender': userinfo.gender,
                                  'course': userinfo.course, 'birthday': userinfo.birthday,
                                  'about_me': userinfo.about_me, 'primaryphoto': userinfo.primaryphoto})
    elif request.method == "POST":
        pf = ProfileEdit(request.POST, request.FILES)
        print request.FILES
        if pf.is_valid():
            userdata = {key:value for (key,value) in pf.cleaned_data.items()}
            if request.FILES.get('primaryphoto',None):
                userinfo.primaryphoto = request.FILES.get('primaryphoto',None)
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
    return render(request, "official/editprofile.html", {'pf': pf})


def image_handler(imagename):
    file_name, file_ext = os.path.splitext(imagename)
    im = Image.open(imagename)
    if file_ext.lower() in [".png", ".gif"]:
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, im)
    else:
        bg = im
    image_resize(bg, (160, 160), imagename)
    thumb_sizes = [(64, 64), (32, 32)]
    for thumb_size in thumb_sizes:
        thumb_name = "thumb_%s" % (thumb_size[0])
        imgname = file_name + thumb_name + file_ext
        image_resize(bg, thumb_size, imgname)


def image_resize(image, size, imagename):
    image = image.resize(size, Image.ANTIALIAS)
    image.save(imagename, "JPEG")
