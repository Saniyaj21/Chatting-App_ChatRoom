from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, null=True,blank = True, on_delete=models.CASCADE)
    fullName = models.CharField(max_length = 200, null=True)
    email = models.EmailField(max_length =100, null=True)
    dp = models.ImageField(null = True, blank = True,default='bydefault.jpg',upload_to="media")
    
    
    def __str__(self):
        return self.user.username 



class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    password = models.CharField( max_length=50, null=True, blank=True)
    participents= models.ManyToManyField(User, related_name='participents',blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    user=models.ForeignKey(User, on_delete= models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #cascade for parent deleted then childs will be deleted
    body = models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body


class Feedback(models.Model):
    name=models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=500)
    
    def __str__(self):
        return self.feedback