import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm, Textarea, CharField
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import User, Post


class CreatePostForm(ModelForm):
    '''Django form for create a new post'''
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={
                'placeholder': 'What are you thinking?'
            })
        }
        labels = {
            'content': ''
        }


def index(request):
    '''Display the homepage. If user logged in, he can create new post and view posts of him/her and friends'''
    

    if request.method == "GET":
        if request.user.is_authenticated:

            followings = request.user.followings.all()
            posts = Post.objects.filter(Q(poster__in=followings)|Q(poster=request.user)).order_by('-date_created')
            return render(request, "network/index.html", {
                'form': CreatePostForm(),
                'posts': posts
            })

        else:
            return render(request,"network/index.html")

    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']

            Post.objects.create(poster=request.user, content=content)

            return redirect(reverse('index'))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def all(request):
    posts = Post.objects.all()
    return render(request, 'network/all.html', {
        'posts': posts
    })


def profile(request, user_id):
    '''User Profile page'''

    owner = User.objects.get(id=user_id)
    posts = Post.objects.filter(poster=owner)
    follower_count = owner.followers.all().count()


    return render(request, 'network/profile.html', {
        'owner': owner,
        'posts': posts,
        'follower_count': follower_count

    })


@login_required
def like(request):
    '''Return an JSON respone for like button fetch API'''
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        post = Post.objects.get(id=id)

        # Check if post is in User liked list
        if post in request.user.liked.all(): 
            post.like = post.like - 1
            post.save(update_fields=['like'])
            request.user.liked.remove(post)
            return JsonResponse({"message": "UnLiked.", "id": id, "like_count": post.like})
        else:
            request.user.liked.add(post)
            post.like = post.like + 1
            post.save(update_fields=['like'])
            return JsonResponse({"message": "liked.", "id": id, "like_count": post.like})

    else:
        return JsonResponse({'error': 'POST request required'})

@login_required
def edit(request):
    '''update new content for a post'''
    
    if request.method == 'POST':
        data = json.loads(request.body)

        id = data.get('id')
        new_content = data.get('content')

        post = Post.objects.get(id=id)
        post.content = new_content

        post.save(update_fields=['content'])

        return JsonResponse({'message': 'Post updated'})
        
@login_required
def follow(request):
    '''Follow button'''
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        user = User.objects.get(id = id)
        
        if user in request.user.followings.all():
            request.user.followings.remove(user)
            user.followers.remove(request.user)
            follower_count = user.followers.all().count()
            return JsonResponse({'message': 'unfollowed', 'follower_count': follower_count})
        else:
            request.user.followings.add(user)
            user.followers.add(request.user)
            follower_count = user.followers.all().count()
            return JsonResponse({'message': 'followed', 'follower_count': follower_count})

