import time
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from django import forms

def index(request):
    return render(request, "auctions/index.html",{
        "list":auction_item.objects.all(),
    })

class NewItem(forms.Form):
    name= forms.CharField()
    st_bid=forms.FloatField(label="Starting bid")
    description= forms.CharField(widget=Textarea)


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_item(request):
    if request.method == "POST"  :
        f= NewItem(request.POST)
        if f.is_valid():
            name=f.cleaned_data["name"]
            st_bid=f.cleaned_data["st_bid"]
            description=f.cleaned_data["description"]
            auction_item.objects.create(name=name, cur_bid=st_bid,description=description,created_by=request.user)
            return render(request, "auctions/index.html",{
                "list":auction_item.objects.all(),
            })
    return render(request,"auctions/new.html",{
        "form": NewItem()
    })

