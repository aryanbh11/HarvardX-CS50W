import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import *

POSTS_PER_PAGE = 10


def index(request):
    if not request.user.is_authenticated:
            return render(request, "network/index_logged_out.html")
    return render(request, "network/index.html")


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


def get_posts(request, type, username):
    pages_dict = {}

    if type == 1:
        posts = Posts.objects.all()
        pages = Paginator(posts, POSTS_PER_PAGE)
        
        i = 1
        for page in pages:
            pages_dict[i] = {}
            pages_dict[i]['posts'] = [post.serialize() for post in page.object_list]
            pages_dict[i]['has_next'] = page.has_next()
            pages_dict[i]['has_previous'] = page.has_previous()
            i = i + 1

    elif type == 0:
        following_posts = []
        posts = Posts.objects.all()
        following_userset = UserFollowing.objects.filter(user=request.user)
        following_usernames = []

        for uf in following_userset:
            following_usernames.append(uf.following_user.username)

        for post in posts:
            if post.user.username in following_usernames:
                following_posts.append(post)

        pages = Paginator(following_posts, POSTS_PER_PAGE)
        
        i = 1
        for page in pages:
            pages_dict[i] = {}
            pages_dict[i]['posts'] = [post.serialize() for post in page.object_list]
            pages_dict[i]['has_next'] = page.has_next()
            pages_dict[i]['has_previous'] = page.has_previous()
            i = i + 1

        if len(following_posts) == 0:
            return JsonResponse({"message": "You dont follow anyone. Whats up with that 😂?"}, status=201)

    else:
        user = User.objects.get(username=username)
        posts = user.posts.all()

        pages = Paginator(posts, POSTS_PER_PAGE)
        
        i = 1
        for page in pages:
            pages_dict[i] = {}
            pages_dict[i]['posts'] = [post.serialize() for post in page.object_list]
            pages_dict[i]['has_next'] = page.has_next()
            pages_dict[i]['has_previous'] = page.has_previous()
            i = i + 1

    return JsonResponse(pages_dict, safe=False)


@csrf_exempt
@login_required
def compose(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    post = Posts(
        user=request.user,
        body=data.get("body")
    )

    post.save()

    return JsonResponse({"message": "Posted successfully."}, status=201)


@csrf_exempt
@login_required
def get_post(request, id):
    try:
        post = Posts.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        post.body = data.get("content")
        post.save()
        return JsonResponse({"message": "Edits saved!"}, status=201)


def get_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if user == request.user:
        return JsonResponse(user.serialize_self(), safe=False)

    else:
        return JsonResponse(user.serialize_other(), safe=False)


@csrf_exempt
@login_required
def is_following(request, username_1, username_2):
    try:
        user1 = User.objects.get(username=username_1)
        user2 = User.objects.get(username=username_2)
    except User.DoesNotExist:
        return JsonResponse({"error": "One of the users not found."}, status=404)

    if request.method == "GET":
        try:
            is_following = UserFollowing.objects.get(user=user1, following_user=user2)
            print(is_following)
            return JsonResponse({"is_following": True})
        except UserFollowing.DoesNotExist:
            return JsonResponse({"is_following": False})

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("following") == True:
            instance = UserFollowing.objects.get(user=user1, following_user=user2)
            instance.delete()
            return JsonResponse({"message": "User unfollowed."}, status=201)
        else:
            instance = UserFollowing(user=user1, following_user=user2)
            instance.save()
            return JsonResponse({"message": "User followed!"}, status=201)


@csrf_exempt
@login_required
def likes(request, username, post_id):
    user = User.objects.get(username=username)
    post = Posts.objects.get(id=post_id)

    if request.method == "GET":
        try:
            is_liked = Likes.objects.get(post=post, user=user)
            return JsonResponse({"is_liked": True})
        except Likes.DoesNotExist:
            return JsonResponse({"is_liked": False})

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("liked") == True:
            instance = Likes.objects.get(post=post, user=user)
            instance.delete()
            return JsonResponse({"message": "Post unliked."}, status=201)
        else:
            instance = Likes(post=post, user=user)
            instance.save()
            return JsonResponse({"message": "Post Liked!"}, status=201)
