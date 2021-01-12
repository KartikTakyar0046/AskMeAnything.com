from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from django.http import HttpResponseRedirect
import json
from django.urls import reverse
from django.views.generic import ListView,DetailView
from .forms import  *
from user.models import *
from .models import *
def homepage(request):
    return render(request,'base.html')

def all_user(request):
    logged_user=request.user
    profile_users=Profile.objects.all()
    users=User.objects.all()
    context={'users':users}
    return render(request,'all_users.html',context)
def follow(request, username):


    main_user = request.user
    to_follow = User.objects.get(username = username)

    #check if already following
    following = Follow.objects.filter(following=main_user, follower=to_follow)
    is_following = True if following else False

    if is_following:
        following.delete()
        is_following = False

    else:
        follow_obj=Follow(following=main_user,follower=to_follow)
        follow_obj.save()
        is_following = True

    resp = {
        "following" : is_following,
    }
    return redirect('profile-visit',username=to_follow)

class HomeView(ListView):
    model=Question
    template_name = 'home.html'


def detailedquestion(request,pk):
    user_visit=request.user
    quest=Question.objects.get(pk=pk)
    answrs=Answer.objects.filter(question=quest)
    context={'quest':quest,'answrs':answrs,'user_visit':user_visit}
    return render(request,'detailed.html',context=context)
def askquestion(request):
    user_asking=request.user
    form = AskQuestionForm(request.POST)
    if request.method=='POST':
        post=form.save(commit=False)
        post.author=user_asking
        post.save()
        return redirect('home')
    context={'form':form}
    return render(request,'askquestion.html',context=context)

def addAnswer(request,pk):
    ques=Question.objects.get(pk=pk)
    user_visit=request.user
    form=AddAnswer(request.POST)
    if request.method=='POST':
        post=form.save(commit=False)
        post.publisher=user_visit
        post.question=ques
        post.save()
        return redirect('question-detail' ,pk=pk)
    context={'form':form}
    return render(request,'addanswer.html',context=context)

def upvote(request,pk):
    ans=Answer.objects.get(id=pk)
    quest_id=ans.question.id
    ans.downvotes.remove(request.user)
    ans.upvotes.add(request.user)
    return HttpResponseRedirect(reverse('question-detail',args=[str(quest_id)]))
def downvote(request,pk):
    ans=Answer.objects.get(id=pk)
    quest_id=ans.question.id
    ans.upvotes.remove(request.user)
    ans.downvotes.add(request.user)
    return HttpResponseRedirect(reverse('question-detail',args=[str(quest_id)]))