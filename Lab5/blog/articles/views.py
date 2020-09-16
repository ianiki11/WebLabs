# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Article


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
