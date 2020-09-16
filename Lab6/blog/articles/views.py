# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


# Create your views here.
def archive(request):
    return render(request, 'archive.html', {"posts":Article.objects.all()})
    

def get_article(request, article_id):
    try:                
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404


def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"],
                'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            posts = Article.objects.all()
            if form['title'] in [post.title for post in posts]:
                form['errors'] = "Статья с таким заголовком уже существует"
                return render(request, 'create_post.html', {'form': form})

            if form["text"] and form["title"]:
                # если поля заполнены без ошибок
                article = Article.objects.create(text=form["text"],
                                    title=form["title"],
                                    author=request.user)
                return redirect('get_article', article_id=article.id)
                # перейти на страницу поста

            # если введенные данные некорректны
            form['errors'] = "Не все поля заполнены"
            return render(request, 'create_post.html', {'form': form})

        # просто вернуть страницу с формой, если метод GET
        return render(request, 'create_post.html', {})
    else:
        raise Http404
        
def register_user(request):
    #if request.user and request.user.is_anonymous:
    #    return redirect('index')
    
    if request.method == 'POST':
        form = {
            'username': request.POST['username'],
            'password': request.POST['password'],
            'password_confirm': request.POST['password_confirm'],
        }
        try:
            User.objects.get(username=form['username'])
            form['errors'] = "Пользователь с таким именем уже существует"
            return render(request, 'register.html', {'form': form})
        except:
            pass

        if form['password'] != form['password_confirm']:
            form['errors'] = "Пароли не совпадают"
            return render(request, 'register.html', {'form': form})

        if form['username'] and form['password'] and form['password_confirm']:
            User.objects.create_user(
                username=form['username'],
                password=form['password'],
            )
            return redirect('login-page')
        form['errors'] = "Не все поля заполнены"
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {})


def auth_user(request):
    if request.method == 'POST':
        form = {
            'username': request.POST['username'],
            'password': request.POST['password'],
        }
    
        if form['username'] and form['password']:
            user = authenticate(username=form['username'], password=form['password'])
            if user:
                login(request, user)
                return redirect('index')
            form['errors'] = "Не все поля заполнены"
        form['errors'] = "Нет аккаунта с таким сочетанием никнейма и пароля"
        return render(request, 'auth.html', {'form': form})
    return render(request, 'auth.html', {})