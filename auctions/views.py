from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
import os

from . models import *


def index(request):
    user = request.user
    if not request.user.is_authenticated:
        return render(request, "auctions/index.html", {
            "auctions": Listings.objects.all(),
        })
    return render(request, "auctions/index.html", {
        "auctions": Listings.objects.all(),
        "count": Watchlist.objects.filter(user=user).count()
    })


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


@login_required
def new_listing(request):
    user = request.user
    if request.method == "POST":
        newtitle = request.POST.get("newtitle")
        descript = request.POST.get("descript")
        bids = request.POST.get("newbid")
        tag = request.POST.get("tag")
        img = request.FILES.get("image")

        f = Listings(title=newtitle, description=descript,
                     starter_bid=bids, image=img, user=user)
        x = Bid(bid=f, user=user, lastbid=bids)
        z = Img(img=f)
        y = Tags(tags=tag, auction=f)
        f.save()
        x.save()
        z.save()
        y.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/new_listing.html", {
        "count": Watchlist.objects.filter(user=user).count(),
    })


def auctionpage(request):
    user = request.user
    if request.method == "GET":
        contentid = request.GET.get("hidden")
        firstbid = Listings.objects.get(id=contentid)
        return render(request, "auctions/auctionpage.html", {
            "auction": Listings.objects.get(id=contentid),
            "bid": Bid.objects.get(bid=contentid),
            "count": Watchlist.objects.filter(user=user).count(),
            "comments": Comments.objects.filter(auction=contentid),
            "tags": Tags.objects.filter(auction=firstbid),
            "user": user
        })
    if request.method == "POST":
        placed_bid = int(request.POST.get("newbid"))
        auctionid = request.POST.get("auctionid")
        f = Listings.objects.get(id=auctionid)
        bid = Bid.objects.get(bid=f)
        if placed_bid > bid.lastbid:
            Bid.objects.filter(bid=f).update(user=user, lastbid=placed_bid)
            return render(request, "auctions/auctionpage.html", {
                "auction": Listings.objects.get(id=auctionid),
                "count": Watchlist.objects.filter(user=user).count(),
                "comments": Comments.objects.filter(auction=auctionid),
                "bid": Bid.objects.get(bid=auctionid),
                "user": user
            })
        else:
            check = 2
            return render(request, "auctions/auctionpage.html", {
                "auction": Listings.objects.get(id=auctionid),
                "count": Watchlist.objects.filter(user=user).count(),
                "comments": Comments.objects.filter(auction=auctionid),
                "bid": Bid.objects.get(bid=auctionid),
                "check": check,
                "user": user
            })


@login_required
def watchlist(request):
    check = 0
    user = request.user
    if request.method == "POST":
        content = request.POST.get("content")
        if not Watchlist.objects.filter(Watchlist=content, user=user).exists():
            f = Listings.objects.get(id=content)
            x = Watchlist(Watchlist=f, user=user)
            x.save()

            return HttpResponseRedirect(reverse("watchlist"))
        else:
            check = 1
            return render(request, "auctions/auctionpage.html", {
                "check": check,
                "auction": Listings.objects.get(id=content),
                "count": Watchlist.objects.filter(user=user).count(),
            })
    return render(request, "auctions/watchlist.html", {
        "auctions": Watchlist.objects.filter(user=user),
        "count": Watchlist.objects.filter(user=user).count(),
    })


@login_required
def delete(request):
    if request.method == "POST":
        content = request.POST.get("hidden")

        f = Watchlist.objects.filter(id=content)
        f.delete()
        return HttpResponseRedirect(reverse("watchlist"))


@login_required
def comment(request):
    user = request.user
    if request.method == "POST":
        comment = request.POST.get("comments")
        listid = request.POST.get("content")
        x = Listings.objects.get(id=listid)
        f = Comments(comments=comment, user=user, auction=x)
        f.save()

        return render(request, 'auctions/auctionpage.html', {
            "comments": Comments.objects.filter(auction=listid),
            "auction": Listings.objects.get(id=listid),
            "count": Watchlist.objects.filter(user=user).count(),
        })


@login_required
def close(request):
    if request.method == "POST":
        auctionid = request.POST.get("auctionid")
        user = Bid.objects.get(bid=auctionid)
        f = Listings.objects.get(id=auctionid)
        last_bid = user.lastbid
        f.delete()

        return render(request, 'auctions/winner.html', {
            "highest": last_bid,
            "user": user.user

        })


def tags(request):
    user = request.user
    if request.method == 'GET':
        tagname = request.GET.get("tagname")
        return render(request, "auctions/Tag.html", {
            "tags": Tags.objects.filter(tags=tagname),
            "count": Watchlist.objects.filter(user=user).count(),

        })
