from django.db import models
from django.contrib.auth.models import  User
# Create your models here.

class Question(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=255)
    published_date=models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.body)+ " by "+ str(self.author)


class Answer(models.Model):
    question=models.ForeignKey(Question,related_name="answers",on_delete=models.CASCADE)
    body=models.TextField()
    published_date=models.DateField(auto_now_add=True)
    publisher=models.ForeignKey(User,on_delete=models.CASCADE)
    upvotes=models.ManyToManyField(User,related_name="upvote")
    def total_upvotes(self):
        return self.upvotes.count
    downvotes=models.ManyToManyField(User,related_name="downvote")
    def __str__(self):
        return '%s - %s - %s'%(self.question.body,self.publisher,self.body)