from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User, Thread
import json
pages = 10

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['body']

def following_view(request):
    threads_list = Thread.objects.filter(creator__in = request.user.following.all()).order_by('-timestamp')
    paginator = Paginator(threads_list, pages)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
    })
    

def index(request):
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.creator = request.user
            thread.save()
        else:
            return JsonResponse({
                "error": "form not valid"
            })

    threads_list = Thread.objects.all().order_by('-timestamp')
    paginator = Paginator(threads_list, pages)  # Show "pages" threads per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{
        "AddPostForm" : ThreadForm(),
        "page_obj": page_obj,
    })


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

def profile(request,username):
    user1 = User.objects.get(username = username)
    threads_list = Thread.objects.filter(creator = user1).order_by('-timestamp')
    paginator = Paginator(threads_list, pages)  # Show 10 threads per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html",{
        "user": user1,
        "following_count" : user1.following.all().count(),
        "follower_count" : user1.followers.all().count(),
        "page_obj" : page_obj,
        "request_user_following": request.user.following.all()
    })

#API ROUTES
@csrf_exempt
def thread_view(request, thread_id):
    try:
        thread = Thread.objects.get(pk = thread_id)
    except Thread.DoesNotExist:
        return JsonResponse({"error":"Thread Not Found!"}, status=404)

    
    if request.method == "GET":
        return JsonResponse(thread.serialize(), safe=False)
    elif request.method == "PUT":
        try:
            thread = Thread.objects.get(pk = thread_id)
        except Thread.DoesNotExist:
            return JsonResponse({"error":"Thread Not Found!"}, status=404)
        
        if request.user in thread.likes.all():
            thread.likes.remove(request.user)
            thread.like_count -= 1
            liked = False
        else:
            thread.likes.add(request.user)
            thread.like_count += 1
            liked = True
        
        thread.save()
        return JsonResponse({"like_count":thread.like_count,"liked":liked})
    else:
        return JsonResponse({"error": "PUT/GET request required."}, status=400)

@csrf_exempt
def user_api(request, user_id):
    try:
        user1 = User.objects.get(pk = user_id)
    except:
        return JsonResponse({"error":"User Not Found!"}, status=404)

    if request.method == "PUT":
        if user1 in request.user.following.all():
            request.user.following.remove(user1)
            followin = False
        else:
            request.user.following.add(user1)
            followin = True
        
        request.user.save()
        user1.save()
        return JsonResponse({
            "following":followin,
            "follower_count" : user1.followers.all().count(),
        })
    else:
        JsonResponse({"error": "PUT request required."}, status=400)

@csrf_exempt
def edit_api(request,thread_id):
    try:
        thread = Thread.objects.get(pk = thread_id)
    except Thread.DoesNotExist:
        return JsonResponse({"error":"Thread Not Found!"}, status=404)

    # Making sure if user is the owner of the thread or not
    if thread.creator != request.user:
        return JsonResponse({
            "error":"You are not the creator of this thread"
        })

    if request.method == "PUT":
        if request.content_type == "application/json":
            data = json.loads(request.body.decode('utf-8'))
            text = data.get("text", "")
            thread.body = text
            thread.save()
            return JsonResponse({
                "body":text 
            })
        else:
            return JsonResponse({"error":"Data type not ok"})
    else:
        return JsonResponse({
            "error":"Invalid method of request!"
        })