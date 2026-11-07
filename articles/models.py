from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(null=True, upload_to="articles/")
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ("-created_at",)


class Category(models.Model):
    name = models.CharField()



class Comment(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE, null=True)
    author_name = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.author_name

    class Meta:
        ordering = ("-created_at",)

