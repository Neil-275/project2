from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class categories(models.Model):
    name= models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"

class auction_item(models.Model):
    name= models.CharField(max_length=64)
    cur_bid=models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)
    description= models.TextField(max_length=500)
    created_by= models.ForeignKey(User,on_delete=models.CASCADE,default=0)
    img= models.URLField(blank=False, default="")
    liked= models.ManyToManyField(User,related_name="watchlist",blank= True)
    closed= models.IntegerField(default=0)
    classify= models.ForeignKey(categories, on_delete=models.CASCADE,related_name="item",null=True)
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


