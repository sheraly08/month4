from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from articles.forms import ArticleForm, CommentForm
from articles.models import Article, Category, Comment
from typing import Any  
from django.db.models import Q
from django.contrib.auth.models import User 
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
class ArticleListView(ListView):
    template_name = "articles/list.html"
    model = Article
    context_object_name = "articles"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        context["users"] = User.objects.all()
        return context

    def get_queryset(self) -> QuerySet[Any, Any]:
        qs = super().get_queryset()
        if search := self.request.GET.get("q"):
            title = Q(title__icontains=search)
            text = Q(text__icontains=search)
            qs = qs.filter(text | title)

        if rate := self.request.GET.get("rate"):
            sort = self.request.GET.get("sort")

            if sort == "gt":
                qs = qs.filter(rate__gte=rate)
            else:
                qs = qs.filter(rate__lte=rate)

        if category_id := self.request.GET.get("category"):
            qs = qs.filter(category=category_id)

        if authors := self.request.GET.getlist("users"):
            qs = qs.filter(user_id__in=authors)

        return qs


class ArticleCreateView(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = "articles/create.html"
    success_url = reverse_lazy("article_list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"
    context_object_name = "article"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context['comments'] = Comment.objects.filter(article=self.object).select_related("user")

        context["form"] = CommentForm()

        return context

class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/edit.html"
    pk_url_kwarg = "id"


    def test_func(self):
        article = self.get_object()
        return self.request.user == article.user

    def get_success_url(self):
        return reverse_lazy("article_detail", kwargs={"id":self.object.id})
       

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "articles/delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("article_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("article_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        messages.success(self.request, "Добро пожаловать! Аккаунт создан.")
        return response


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = "articles/comment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article"] = get_object_or_404(Article, id=self.kwargs["id"])
        return context

    def form_valid(self, form):
        form.instance.article = get_object_or_404(Article, id=self.kwargs["id"])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("article_detail", kwargs={"id": self.kwargs["id"]})


class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "articles/comment_edit.html"
    pk_url_kwarg = "id_comment"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        return reverse_lazy("article_detail", kwargs={"id": self.kwargs["id"]})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "articles/comment_delete.html"
    pk_url_kwarg = "id_comment"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        return reverse_lazy("article_detail", kwargs={"id": self.kwargs["id"]})


class MyCommentListView(LoginRequiredMixin, ListView):
    template_name = "comments/list.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user).select_related("article")
