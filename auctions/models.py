from email.policy import default
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auction_item(models.Model):
    name= models.CharField(max_length=64)
    cur_bid=models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)
    description= models.TextField(max_length=500)
    created_by= models.ForeignKey(User,on_delete=models.CASCADE,default=0)
    img= models.URLField(blank=False, default="")
    liked= models.ForeignKey(User,on_delete= models.CASCADE,related_name="watchlist",null=True,blank= True)
    closed= models.IntegerField(default=0)

    def __str__ (self):    
        return (str) (f"{self.name}  \n Price:{self.bidset.last()}$ \n ")
        

class info_bid(models.Model):
    who= models.ForeignKey(User,on_delete=models.CASCADE,default=0)
    bid= models.FloatField()
    item=models.ForeignKey(auction_item, on_delete= models.CASCADE,related_name="bidset")
    
    def __str__ (self):
        return f"{self.bid}"
    
class cmt(models.Model):
    item= models.ForeignKey(auction_item, on_delete= models.CASCADE,related_name="cmt")
    comment= models.TextField(max_length=500)
    posted_by= models.ForeignKey(User,on_delete=models.CASCADE)
    date= models.DateTimeField(auto_now_add= True)

class categories(models.Model):
    name= models.CharField(max_length=64)
    item= models.ManyToManyField(auction_item,related_name="classify")
     
    def __str__(self):
        return f"{self.name}"
