from django.db import models
from django.conrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

article = 'AR'
news = 'NE'

POST = [
    (news, 'Новость'),
    (article, 'Статья ')
]


# class User(models.Model):
#     pass

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delate=models.CASCADE)
    rating_autor = models.IntegerField(default=0)
    def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rating_post') * 3, 0))
        author_comment_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comment_rating_sum=Coalesce(Sum('rating_comment'),0))
        author_post_comment_rating = Comment.objects.filter(post__author__name=self.user).aggregate(
            comment_rating_sum=Coalesce(Sum('rating_comment'),0))
        self.rating_autor = author_posts_rating['post_rating_sum'] + author_comment_rating['comments+rating_sum'] + author_post_comment_rating['comments_rating_sum']
        self.save()

class Category(models.Model):
    name = models.CharFild(max_length=200, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    data = models.DataTimefield(auto_now_add=True)
    title = models.CharFild(max_length=200)
    type = models.CharFild(max_length=2, choices=POST)
    text = models.TextField()
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.seve()

    def dislike(self):
        self.rating -= 1
        self.seve()

    def preview(self):
        return self.text[:124]

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delet=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_in_comment = models.DataTimefield(auto_now_add=True)
    rating_comment = models.IntegerField(defailt=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()