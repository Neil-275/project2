from email.policy import default
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

    def __str__ (self):
        return f"{self.name}"

class info_bid(models.Model):
    who= models.ForeignKey(User,on_delete=models.CASCADE,default=0)
    bid= models.FloatField()
    item=models.ForeignKey(auction_item, on_delete= models.CASCADE)
    
class cmt(models.Model):
    item= models.ForeignKey(auction_item, on_delete= models.CASCADE)
    comment= models.TextField(max_length=500)
    posted_by= models.IntegerField()
    date= models.DateTimeField(auto_now_add= True)



    


    
