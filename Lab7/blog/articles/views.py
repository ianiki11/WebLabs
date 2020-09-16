# Create your views here.
from articles.models import Article
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404


def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})


def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = {'text': request.POST["text"], 'title': request.POST["title"]}
            if form["text"] and form["title"]:
                article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return get_article(request, article.id)
            else:
                form['errors'] = "Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            return render(request, 'create_post.html', {})
    else:
        raise Http404




def login_user(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = {'name': request.POST["name"], 'password': request.POST["password"]}
            if form["name"] and form['password']:
                try:
                    User.objects.get(username=form['name'])
                    user = authenticate(username=form['name'], password=form['password'])
                    if login(request, user) is None:
                        form['errors'] = "Некорректные данные"
                        return render(request, 'login.html', {'form': form})
                    else:
                        return archive(request)
                except User.DoesNotExist:
                    form['errors'] = "Пользователь существует"
                    return render(request, 'create_user.html', {'form': form})
            else:
                form['errors'] = "Не все поля заполнены"
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {})
    else:
        return archive(request)


def register(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = {'email': request.POST["email"], 'name': request.POST["name"], 'password': request.POST["password"]}
            if form["name"] and form["email"] and form['password']:
                try:
                    User.objects.get(username=form['name'])
                    form['errors'] = "пользователь существует"
                    return render(request, 'create_user.html', {'form': form})
                except User.DoesNotExist:
                    User.objects.create_user(form['name'], form['email'], form['password'])
                    return render(request, 'login.html')
            else:
                form['errors'] = "Не все поля заполнены"
                return render(request, 'create_user.html', {'form': form})
        else:
            return render(request, 'create_user.html', {})
    else:
        return archive(request)