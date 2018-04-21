# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import re
from datetime import date

# Create your models here.

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def check_registration(self, userInfo, request):
        valid = True
        today = date.today().strftime("%Y-%m-%d")
        
        if not userInfo['name'].isalpha():
            messages.warning(request, "Your name must be only letters. ")
            valid = False
        if len(userInfo['name']) < 2:
            messages.warning(request, "Your name must be 2 or more characters long.")
            valid = False
        if not userInfo['alias'].isalpha():
            messages.warning(request, "Your alias must be all letters.")
            valid = False
        if len(userInfo['alias']) < 2:
            messages.warning(request, "Your alias must be 2 or more characters long!")
            valid = False
        if not EMAIL_REGEX.match(userInfo['email']):
            messages.warning(request, "Your email is not valid.")
            valid = False
        if len(userInfo['password']) < 8:
            messages.warning(request, "Your password is too short.")
            valid = False
        if userInfo['password'] != userInfo['confirm_password']:
            messages.warning(request, "Your passwords do not match.")
            valid = False
        if userInfo['dob'] == '':
            messages.warning(request, "You must enter your date of birth.")
            valid = False
        if userInfo['dob'] >= today:
            messages.warning(request, "You cannot enter today's date or a date in the future.")
            valid = False
        print "*"*10
        print userInfo['dob']
        print "*"*10
        if User.objects.filter(email = userInfo['email']):
            messages.error(request, "The email you have entered already exists.")
            valid = False
        
        if valid == True:
            hashed = bcrypt.hashpw(userInfo['password'].encode(), bcrypt.gensalt())
            User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed, dob = request.POST['dob'])
        return valid

    def check_login(self, userInfo, request):
        valid = True
        
        if User.objects.filter(email = userInfo['email']):
            hashed = User.objects.get(email = userInfo['email']).password
            hashed = hashed.encode('utf-8')
            password = userInfo['password']
            password = password.encode('utf-8')
            if bcrypt.hashpw(password, hashed) == hashed:
                valid = True
            else:
                messages.warning(request, "Incorrect password. Please try again.")
                valid = False
        else:
            messages.warning(request, "Incorrect email address. Please try again.")
            valid = False
        return valid

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    dob = models.DateField()
    friend_of = models.ManyToManyField('self', related_name = "friend_to")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    UserManager = UserManager()
    objects = models.Manager()