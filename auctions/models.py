from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction", blank=True, related_name="users")
    

class Category(models.Model):
    name = models.CharField(max_length=64)


class Auction(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField()
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name="categories")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authors")
    is_sold = models.BooleanField(default=False)
    publication_date = models.DateTimeField( null=True, blank=True)
    comments = models.ManyToManyField("Comment", related_name="comments")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="winner", null=True, blank=True)

    

class Bid(models.Model):
    auctuion = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    price = models.IntegerField()
    

class Comment(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auctions")


