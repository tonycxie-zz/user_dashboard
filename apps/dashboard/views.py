from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..signin.models import *
import bcrypt


def index(request):
    if request.session.get("userid"):
        user = Users.objects.get(id = request.session["userid"])
    else:
        user = Users.objects.get(email = request.session["email"])
    request.session["user_level"] = user.user_level
    request.session["first_name"] = user.first_name
    request.session["last_name"] = user.last_name
    request.session["email"] = user.email
    return render(request, "dashboard/index.html", { "users": Users.objects.all() })


def logout(request):
    request.session.flush()
    return redirect("/")