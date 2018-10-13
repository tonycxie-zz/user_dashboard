from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..signin.models import *
import bcrypt


def new(request):
    if request.session["user_level"] == 9:
        return render(request, "users/new.html")
    return redirect("/dashboard")


def create_user(request):
    if request.method == "POST":
        user_level = 1
        if Users.objects.all().count() == 0:
            user_level = 9 
        errors = Users.objects.register_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/register")
        pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        Users.objects.create(
            first_name = request.POST["first_name"], 
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            birthday = request.POST["birthday"],
            user_level = user_level,
            password_hash = pw_hash
        )
    return redirect("/dashboard")


def edit(request):
    request.session["user_or_self"] = "self"
    return render(request, "users/edit.html")


def edit_info(request, number):
    if request.method == "POST":
        errors = Users.objects.info_validator(request.POST, request.session["email"])
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            if request.session["user_or_self"] == "user":
                return redirect("/users/edit_user/" + number)
            else:
                return redirect("/users/edit")
        user = Users.objects.get(id = number)
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        user.birthday = request.POST["birthday"]
        if request.POST["user_level"]:
            if request.POST["user_level"] == "admin":
                user.user_level = 9
            else:
                user.user_level = 1
        user.save()
        request.session["first_name"] = user.first_name
        request.session["last_name"] = user.last_name
        request.session["email"] = user.email
        request.session["birthday"] = user.birthday
    return redirect("/dashboard")


def edit_pw(request, number):
    if request.method == "POST":
        errors = Users.objects.pw_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            if request.session["user_or_self"] == "user":
                return redirect("/users/edit_user/" + number)
            else:
                return redirect("/users/edit")
        pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        user = Users.objects.get(id = number)
        user.password_hash = pw_hash
        user.save()
    return redirect("/dashboard")


def edit_desc(request, number):
    if request.method == "POST":
        user = Users.objects.get(id = number)
        user.desc = request.POST["desc"]
        user.save()
    return redirect("/dashboard")


def edit_user(request, number):
    user = Users.objects.get(id = number)
    request.session["user_or_self"] = "user"
    request.session["first_name"] = user.first_name
    request.session["last_name"] = user.last_name
    request.session["email"] = user.email
    return render(request, "users/edit.html", {"userid": number})


def delete_user(request, number):
    user = Users.objects.get(id = number).delete()
    return redirect("/dashboard")


def make_admin(request, number):
    user = Users.objects.get(id = number)
    user.user_level = 9
    user.save()
    return redirect("/dashboard")


def remove_admin(request, number):
    user = Users.objects.get(id = number)
    user.user_level = 1
    user.save()
    return redirect("/dashboard")


def show_user(request, number):
    user = Users.objects.get(id = number)
    context = {
        "user": user,
        "posted_messages": Messages.objects.filter(receive_message_user_id = user.id)
    }
    return render(request, "users/show.html", context)


def post_message(request):
    if request.method == "POST":
        Messages.objects.create(
            message = request.POST["message"],
            receive_message_user_id = request.POST["receive_id"],
            send_message_user_id = request.session["userid"]
        )
    return redirect("/users/show/" + request.POST["receive_id"])


def post_comment(request):
    if request.method == "POST":
        Comments.objects.create(
            comment = request.POST["comment"],
            commenting_user_id = request.session["userid"],
            comments_message_id = request.POST["message_id"]
        )
    return redirect("/users/show/" + request.POST["receive_id"])


def delete_message(request, number):
    message = Messages.objects.get(id = number)
    userid = message.receive_message_user_id
    message.delete()
    return redirect("/users/show/" + str(userid))


def delete_comment(request, number):
    comment = Comments.objects.get(id = number)
    userid = comment.comments_message.receive_message_user_id
    comment.delete()
    return redirect("/users/show/" + str(userid))