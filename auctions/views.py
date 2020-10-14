from django.contrib import auth
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import AuctionForm, CommentForm
from .models import User, Auction, Bid, Comment
from datetime import datetime
from django.utils.timezone import now
from .helper import get_acuction_context


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all(),
    })


def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        auth.login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = Auction(
                            name = form.cleaned_data["name"],
                            description = form.cleaned_data["description"],
                            price = form.cleaned_data["price"],
                            image = form.cleaned_data["image"],
                            category = form.cleaned_data["category"],
                            author = auth.get_user(request),
                            publication_date = now,
                            isSold = False)
            auction.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            print(form.errors)
            return HttpResponse(form.errors)
    else:
        context = {} 
        context['form'] = AuctionForm()
        return render(request, "auctions/create.html", context)    


def auction(request, auction_id):
    context = get_acuction_context(request, auction_id)
    user = context["user"]
    auction_details = context["details"]
    if user.is_authenticated:
        if auction_details in user.watchlist.all():
            context["button"] = "Remove from watchlist"
        else:
            context["button"] = "Add to watchlist"     
    else:
        context["style"] = "display:none"
        context["button"] = ""  
    return render(request, "auctions/auction.html", context)


def add_to_watchlist(request, auction_id):
    auction_details = Auction.objects.filter(id=auction_id)[0]
    user = auth.get_user(request)

    if auction_details in user.watchlist.all():
            user.watchlist.remove(auction_details)
    else:
        user.watchlist.add(auction_details)

    return auction(request, auction_id)   


def add_comment(request, auction_id):
    context = get_acuction_context(request, auction_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        print("e valid")
        comment = Comment(
            user = context["user"],
            title = form.cleaned_data["title"],
            content = form.cleaned_data["content"],
            auction = context["details"]
            )
        comment.save() 
    else:
        print(form.errors)
        return HttpResponse(form.errors)

    return auction(request, auction_id)















