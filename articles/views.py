from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

from articles.forms import ArticleForm, CommentForm
from articles.models import Article, Category, Comment


def articles_list(request: HttpRequest) -> HttpResponse:
    articles_list = Article.objects.all()

    return render(request, "articles/list.html", {"articles": articles_list})


def article_detail(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)
    comments = Comment.objects.filter(article=article)
    form = CommentForm()
    return render(request, "articles/detail.html", {"article": article, "comments": comments, 'form': form})
        

def article_create(request: HttpRequest) -> HttpResponse:
    form = ArticleForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_list")
    return render(request, "articles/create.html", {"form": form})

def article_edit(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)
    comments = Comment.objects.filter(article=article)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_detail", id=form.instance.id)

    return render(request, "articles/edit.html", {"form": form})

def article_delete(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)

    if request.method == "POST":
        article.delete()
        return redirect("article_list")
    
    return render(request, "articles/delete.html", context={"article": article})

def article_comment(request: HttpRequest, id: int) -> HttpResponse:
    article = Article.objects.get(id=id)
   
    
    form = CommentForm(request.POST or None, instance=Comment(article=article))

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_detail", id=article.id)

    return render(request, "articles/comment.html", {'form': form, 'article': article})

def comment_edit(request: HttpRequest, id:int, id_comment: int) -> HttpResponse:
    
    comment = get_object_or_404(Comment, id=id_comment, article_id=id)
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("article_detail", id=id)
    
    return render(request, "articles/comment_edit.html", {'form': form})


    
def delete_comment(request, id, id_comment)-> HttpResponse:
    comment = get_object_or_404(Comment, id=id_comment, article_id=id) 
    if request.method == "POST" :
        comment.delete()
        return redirect("article_detail", id=id)

    return render(request, "articles/comment_delete.html", {"comment": comment})
        

        

        
        
   