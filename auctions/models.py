from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class bid(models.Model):
    org_price= models.FloatField()
    cur_price= models.FloatField()
    num_modifed= models.IntegerField()
    latest= models.IntegerField()
    
class auction_item(models.Model):
    name= models.CharField(max_length=64)
    price=models.OneToOneField(bid,on_delete= models.CASCADE)
    date= models.DateTimeField(auto_now_add=True)
    description= models.CharField(max_length=300)

class cmt(models.Model):
    item= models.ForeignKey(auction_item, on_delete= models.CASCADE)
    comment= models.CharField(max_length=500)
    posted_by= models.IntegerField()
    date= models.DateTimeField(auto_now_add= True)



    


    
