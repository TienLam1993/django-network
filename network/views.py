import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm, Textarea, CharField


from .models import User, Post


class CreatePostForm(ModelForm):
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

    if request.method == "GET":
        return render(request, "network/index.html", {
            'form': CreatePostForm()
        })

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
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(poster=user)

    return render(request, 'network/profile.html', {
        'user': user,
        'posts': posts

    })



def like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        post = Post.objects.get(id=id)

        post.like = post.like + 1
        post.save(update_fields=['like'])

        return JsonResponse({"message": "liked.", "id": id, "like_count": post.like})

    else:
        return JsonResponse({'error': 'POST request required'})


def edit():
    pass
