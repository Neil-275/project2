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
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "auctions/index.html",{
        "list":auction_item.objects.all(),
    })

choices= categories.objects.all()


class NewItem(forms.Form):
    name= forms.CharField()
    st_bid=forms.FloatField(label="Starting bid")
    description= forms.CharField(widget=Textarea)
    img=forms.URLField(label="Image")
    category=forms.ChoiceField(choices=choices.values_list())

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

@login_required(login_url='login')
def new_item(request):
    if request.method == "POST"  :
        f= NewItem(request.POST)
        if f.is_valid():
            name=f.cleaned_data["name"]
            st_bid=f.cleaned_data["st_bid"]
            description=f.cleaned_data["description"]
            category=f.cleaned_data["category"]
            img=f.cleaned_data["img"]
            new=auction_item(name=name, cur_bid=st_bid,description=description,created_by=request.user, img=img)
            new.save()
            category=categories.objects.get(id=category)
            category.item.add(new)
            info_bid.objects.create(who=request.user,bid=st_bid,item=new)
            return render(request, "auctions/index.html",{
                "list":auction_item.objects.all(),
            })
    return render(request,"auctions/new.html",{
        "form": NewItem()
    })

@login_required(login_url='/login')
def added(request,item):
    s=""
    user=request.user
    try:
        user.watchlist.get(id=item.id)
    except ObjectDoesNotExist:
        s="Add to your watchlist"
    else:
        s="Remove from your watchlist"
    return s

@login_required(login_url='login')
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
    
@login_required(login_url='login')
def addwatchlist(request,idx):
    user=request.user
    item=auction_item.objects.get(id=idx)
    s=added(request,item)
    if s=="Remove from your watchlist":
        user.watchlist.remove(item)
    else :
        user.watchlist.add(item)
    return HttpResponseRedirect(reverse('item',kwargs={"idx": idx}))

@login_required(login_url='login')
def watchlist (request):
    user=request.user
    return render(request, "auctions/watchlist.html",{
        "list": user.watchlist.all()
    })

@login_required(login_url='login')
def closebid(request,idx):
    item= auction_item.objects.get(id=idx)
    item.closed=1
    item.save()
    return HttpResponseRedirect(reverse('item',kwargs={"idx": idx}))

@login_required(login_url='login')
def comment(request, idx):
    item=auction_item.objects.get(id=idx)
    if request.method=="POST":
        cmt=request.POST["cmt"]
        item.cmt.create(comment=cmt, posted_by= request.user)
        return viewitem(request,idx)

@login_required(login_url='login')
def viewcategories(request):
    return render(request, "auctions/categories.html", {
        "categories": categories.objects.all(),
    })

@login_required(login_url='login')
def categorieslist(request,id):
    return render(request,"auctions/categorieslist.html",{
        "name": categories.objects.get(id=id).name,
        "list": categories.objects.get(id=id).item.all(),
    })