from __future__ import unicode_literals
from django.db import models
from datetime import datetime

class ShowsManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors["title"] = "Show title should be at least 2 characters"
        if len(postData['desc']) < 10:
            errors["desc"] = "Show description should be at least 10 characters"
        #try:
        #    if datetime.strptime(postData['date_show'], "%Y-%m-%d").date() > datetime.today().date():
        #        errors['date_show'] = 'you have to put an older date'
        # except:
        #    errors['date_show'] = 'Set a valid date'
        return errors

class UsersManager(models.Manager):

    def basic_validator(self, postData):
        errors = {}

        if len(postData['name']) < 4:
            errors["name"] = "The user's name should be at least 4 characters lenght"
        if len(postData['email']) < 4:
            errors["email"] = "The user's email should be at least 4 characters lenght"
        if len(postData['password']) < 6:
            errors["password"] = "The user's password should be at least 6 characters lenght"
        if postData['password'] != postData['password_confirm']:
            errors["password"] = "Both passwords should be the same"
        return errors

class Shows(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    desc = models.TextField(default="some tv show")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ShowsManager()

class Networks(models.Model):
    name = models.CharField(max_length = 255)
    shows = models.ForeignKey(Shows, related_name = "networks", on_delete = models.CASCADE, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Users(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UsersManager()