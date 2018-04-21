# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages

# Create your views here.

def index(request):
    if 'name' not in request.session:
        return render(request, 'redo_app/index.html')
    else:
        return render(request, 'redo_app/homepage.html')
    
def register(request):
    if User.UserManager.check_registration(request.POST, request):
        valid = True
        user = User.objects.get(email = request.POST['email'])
        request.session['name'] = user.name
        request.session['user_id'] = user.id
        return redirect('/home')
    else:
        valid = False
        return redirect('/')

def login(request):
    if User.UserManager.check_login(request.POST, request):
        valid = True
        user = User.objects.get(email = request.POST['email'])
        request.session['name'] = user.name
        # request.session['email'] = user.email
        request.session['user_id'] = user.id
        return redirect('/home')
    else:
        valid = False
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def homepage(request):
    if 'name' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['user_id'])
        all_friends = user.friend_of.all()
        not_friends = User.objects.exclude(friend_of = user).exclude(id = request.session['user_id'])
        
        context = {
            'user': user,
            'all_friends': all_friends,
            'not_friends': not_friends
        }
        return render(request, 'redo_app/homepage.html', context)
    
def view_friend(request, id):
    if 'name' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id = id)
    }
    return render(request, 'belt_app/user_profile.html', context)

def add_friend(request, id):
    if 'name' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    friend = User.objects.get(id = id)
    user.friend_of.add(friend)
    return redirect('/home')

def delete_friend(request, id):
    if 'name' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    friend = User.objects.get(id = id)
    user.friend_of.remove(friend)
    return redirect('/home')



