from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now



class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    image = models.FileField(upload_to='images')
    category = models.CharField(max_length=64)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authors")
    isSold = models.BooleanField(default=False)
    pulbication_date = models.DateField(default=now)
    deadline = models.DateField(default=None)
    

class Bid(models.Model):
    auctuion = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    price = models.IntegerField()
    

class Comment(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auctions")