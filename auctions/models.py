from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    starter_bid = models.IntegerField(null=True)
    image = models.ImageField(upload_to='media', blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner", null=True)

    def __str__(self):
        return f"status:{self.id},{self.title},{self.description},{self.starter_bid},{self.image},{self.user}"


class Bid(models.Model):
    bid = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="bids")
    lastbid = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.bid.starter_bid}"


class Img(models.Model):
    img = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="pic", null=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):

        return f"{self.img.image}"


class Watchlist(models.Model):
    Watchlist = models.ForeignKey(Listings, null=True,
                                  on_delete=models.CASCADE, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.Watchlist}"


class Comments(models.Model):
    comments = models.CharField(max_length=500, null=True,)
    auction = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.comments}{self.auction.id}{self.user}"


class Tags(models.Model):
    tags = models.CharField(max_length=20, null=True)
    auction = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True)
