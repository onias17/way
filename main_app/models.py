from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(blank=True, upload_to="images/", default='/images/default-profile-img.png')
    currentcity = models.CharField(max_length=100)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length = 50)
    email = models.EmailField(blank = True)
    slug = models.SlugField(null=True, default='slug')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})


class City(models.Model):
    name = models.CharField(max_length=50, blank=False)
    picture = models.ImageField(upload_to="images/", blank = True, default='/images/shea-rouda-Vtl6cOhO87Y-unsplash.jpg')
    country = models.CharField(max_length=50)
    slug = models.SlugField(null=True, default="slug")

    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("citydetail", kwargs={"slug": self.slug})

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    title = models.CharField( max_length= 200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to="images/", blank=True, default='/images/default.jpg')
    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.title} written by {self.profile.firstname}'

class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(max_length=400)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.profile}s comment on {self.post.profile}s post'