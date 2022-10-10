import time
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django import forms
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return render(request, "auctions/index.html",{
        "list":auction_item.objects.all(),
    })

class NewItem(forms.Form):
    name= forms.CharField()
    st_bid=forms.FloatField(label="Starting bid")
    description= forms.CharField(widget=Textarea)
    img=forms.URLField(label="Image")

class newbid(forms.Form):
    bid= forms.FloatField(label="Place new bid")

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
            new=auction_item(name=name, cur_bid=st_bid,description=description,created_by=request.user)
            new.save()
            info_bid.objects.create(who=request.user,bid=st_bid,item=new)
            return render(request, "auctions/index.html",{
                "list":auction_item.objects.all(),
            })
    return render(request,"auctions/new.html",{
        "form": NewItem()
    })

def added(request,item):
    s=""
    user=request.user
    try:
        user.watchlist.get(id=item.id)
    except ObjectDoesNotExist:
        pass
    else:
        s="Added to your watchlist"
    return s

def viewitem(request,idx):
    item=auction_item.objects.get(pk=idx)
    if request.method=="POST":
        f= newbid(request.POST)
        if f.is_valid():
            bid=f.cleaned_data["bid"]
            cur_bid=float (item.bidset.last().bid)
            if bid<=cur_bid:
                return render( request, "auctions/display.html",{
                    "item":item,
                    "numbid": len(item.bidset.all()),
                    "fail_mess": "You have to place higher than the current bid",
                    "form": f,
                    "wl_mess": added(request,item),
                    
                })
            else: 
                item.bidset.create(who=request.user,bid=bid)
    return render(request, "auctions/display.html",{
    "item": item,
    "numbid": len(item.bidset.all()),
    "form": newbid(),
     "wl_mess": added(request,item)
     })
    
def addwatchlist(request,idx):
    user=request.user
    item=auction_item.objects.get(id=idx)
    s=added(request,item)
    if s=="":
        user.watchlist.create(item)
    return viewitem(request,idx)  

def watchlist (request):
    user=request.user
    return render(request, "auctions/watchlist.html",{
        "list": user.watchlist.all()
    })
   
def closebid(request,idx):
    item= auction_item.objects.get(id=idx)
    item.closed=1
    return viewitem(request,idx)

def comment(request, idx):
    item=auction_item.objects.get(id=idx)
    if request.method=="POST":
        cmt=request.POST["cmt"]
        item.cmt.create(comment=cmt, posted_by= request.user)
        return viewitem(request,idx)
        