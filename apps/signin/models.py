from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime

class UsersManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        NAME_REGEX = re.compile(r'^[a-zA-Z][a-zA-Z]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData["first_name"]) < 1:
            errors["first_name"] = "First name is required"
        elif not NAME_REGEX.match(postData["first_name"]):
            errors["first_name"] = "First name must be at least 2 letters and have no numbers"
        if len(postData["last_name"]) < 1:
            errors["last_name"] = "Last name is required"
        elif not NAME_REGEX.match(postData["last_name"]):
            errors["last_name"] = "Last name must be at least 2 letters and have no numbers"
        if len(postData["email"]) < 1:
            errors["email"] = "Email is required"
        elif not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email"
        elif Users.objects.filter(email = postData["email"]).count() > 0:
            errors["email"] = "Email already exists"
        if len(postData["birthday"]) < 1:
            errors["birthday"] = "Birthday is required"
        elif datetime.strptime(postData["birthday"], "%Y-%m-%d") >= datetime.now():
            errors["birthday"] = "Birthday is invalid"
        if len(postData["password"]) < 1:
            errors["pw"] = "Password is required"
        elif len(postData["password"]) < 9:
            errors["pw"] = "Password must be at least 8 characters"
        if len(postData["confirm_password"]) < 1:
            errors["confirm_pw"] = "You must confirm your password"
        elif postData["password"] != postData["confirm_password"]:
            errors["confirm_pw"] = "Password does not match"
        return errors


    def info_validator(self, postData, email):
        errors = {}
        NAME_REGEX = re.compile(r'^[a-zA-Z][a-zA-Z]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData["first_name"]) < 1:
            errors["first_name"] = "First name is required"
        elif not NAME_REGEX.match(postData["first_name"]):
            errors["first_name"] = "First name must be at least 2 letters and have no numbers"
        if len(postData["last_name"]) < 1:
            errors["last_name"] = "Last name is required"
        elif not NAME_REGEX.match(postData["last_name"]):
            errors["last_name"] = "Last name must be at least 2 letters and have no numbers"
        if len(postData["email"]) < 1:
            errors["email"] = "Email is required"
        elif not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email"
        elif Users.objects.filter(email = postData["email"]).count() > 0 and postData["email"] != email:
            errors["email"] = "Email already exists"
        if len(postData["birthday"]) < 1:
            errors["birthday"] = "Birthday is required"
        elif datetime.strptime(postData["birthday"], "%Y-%m-%d") >= datetime.now():
            errors["birthday"] = "Birthday is invalid"
        return errors


    def pw_validator(self, postData):
        errors = {}
        if len(postData["password"]) < 1:
            errors["pw"] = "Password is required"
        elif len(postData["password"]) < 9:
            errors["pw"] = "Password must be at least 8 characters"
        if len(postData["confirm_password"]) < 1:
            errors["confirm_pw"] = "You must confirm your password"
        elif postData["password"] != postData["confirm_password"]:
            errors["confirm_pw"] = "Password does not match"
        return errors


class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    birthday = models.DateTimeField()
    desc = models.TextField()
    user_level = models.IntegerField()
    password_hash = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UsersManager()

class Messages(models.Model):
    message = models.TextField()
    send_message_user = models.ForeignKey(Users, related_name = "send_users_message")
    receive_message_user = models.ForeignKey(Users, related_name = "receive_users_message")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comments(models.Model):
    comment = models.TextField()
    comments_message = models.ForeignKey(Messages, related_name = "messages_comment")
    commenting_user = models.ForeignKey(Users, related_name = "users_comment")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)