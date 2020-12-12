from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class EasyMoveItem(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    location = models.CharField(max_length=200)
    availability = models.CharField(max_length=200)
    condition = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    item_img = models.ImageField(upload_to='media', blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('EasyMove:item-detail', args=[self.id])

class UserInfo(models.Model):
    ROLE = (
        ('R', 'Regular_user'),
        ('A', 'Admin'),
    )
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=10)
    role = models.CharField(max_length=1, choices=ROLE)



class Comment(models.Model):
    author = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentTitle = models.CharField(max_length=200)
    commentText = models.TextField(blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(EasyMoveItem, on_delete=models.CASCADE)




