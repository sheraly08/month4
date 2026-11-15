from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from articles.forms import ArticleForm, CommentForm
from articles.models import Article, Category, Comment


def articles_list(request: HttpRequest) -> HttpResponse:
    articles_list = Article.objects.select_related("user", "category")

    return render(request, "articles/list.html", {"articles": articles_list})


def article_detail(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)
    comments = Comment.objects.filter(article=article).select_related("user")
    form = CommentForm()
    return render(request, "articles/detail.html", {"article": article, "comments": comments, 'form': form})
        
@login_required
def article_create(request: HttpRequest) -> HttpResponse:
    form = ArticleForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect("article_list")
    return render(request, "articles/create.html", {"form": form})

@login_required
def article_edit(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)

    if request.user != article.user:
        messages.error(request, "Это не ваш пост")
        return redirect("article_detail", id=article.pk)

    
    
    
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_detail", id=form.instance.id)

    return render(request, "articles/edit.html", {"form": form})

@login_required
def article_delete(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)

    if request.user != article.user:
        messages.error(request, "Это не ваш пост")
        return redirect("article_detail", id=article.pk)
        



    if request.method == "POST":
        article.delete()
        return redirect("article_list")
    
    return render(request, "articles/delete.html", context={"article": article})


def signup(request):
    if request.user.is_authenticated:
        return redirect("article_list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Добро пожаловать! Аккаунт создан.")
            return redirect("article_list")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

@login_required
def article_comment(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)


   
    
    form = CommentForm(request.POST or None, instance=Comment(article=article, user=request.user))

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_detail", id=article.id)

    return render(request, "articles/comment.html", {'form': form, 'article': article})

@login_required
def comment_edit(request: HttpRequest, id:int, id_comment: int) -> HttpResponse:
    
    comment = get_object_or_404(Comment, id=id_comment, article_id=id)

    if request.user != comment.user:
        messages.error(request, "Это не ваш комментарий")
        return redirect("article_detail", id=comment.article.pk)


    form = CommentForm(request.POST or None, instance=comment)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_detail", id=id)
    
    return render(request, "articles/comment_edit.html", {'form': form})


@login_required
def delete_comment(request, id, id_comment)-> HttpResponse:
    comment = get_object_or_404(Comment, id=id_comment, article_id=id) 

    if request.user != comment.user:
        messages.error(request, "Это не ваш комментарий")
        return redirect("article_detail", id=comment.article.pk)
    
    if request.method == "POST" :
        comment.delete()
        return redirect("article_detail", id=id)

    return render(request, "articles/comment_delete.html", {"comment": comment})
        

@login_required        
def my_list(request):
    comments = Comment.objects.filter(user=request.user).select_related("article")
    return render(request, "comments/list.html", {"comments": comments})
        
        
   