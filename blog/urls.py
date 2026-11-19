"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from articles.views import (ArticleCreateView, ArticleDetailView, ArticleListView, CommentCreateView,
                            ArticleDeleteView, ArticleEditView, CommentEditView, CommentDeleteView,
                            MyCommentListView, SignUpView
                            )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ArticleListView.as_view(), name="article_list"),
    path("<int:id>/detail", ArticleDetailView.as_view(), name="article_detail"),
    path("create/", ArticleCreateView.as_view(), name="article_create"),
    path("<int:id>/edit", ArticleEditView.as_view(), name="article_edit"),
    path("<int:id>/delete", ArticleDeleteView.as_view(), name="article_delete"),
    path("articles/<int:id>/comment", CommentCreateView.as_view(), name="article_comment"),
    path('articles/<int:id>/comment/<int:id_comment>/edit/', CommentEditView.as_view(), name="comment_edit"),
    path("articles/<int:id>/comment/<int:id_comment>/delete/", CommentDeleteView.as_view(), name="comment_delete" ),
    path("my-comments/", MyCommentListView.as_view(), name="comments_list"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
     path("accounts/", include("django.contrib.auth.urls")),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)