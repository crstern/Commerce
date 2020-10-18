from django.contrib import auth
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import AuctionForm, CommentForm, BidForm
from .models import User, Auction, Bid, Comment
from datetime import datetime
from datetime import datetime
from .helper import get_auction_context, can_be_sold
from django.contrib import messages



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
    print("yo")
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
                            publication_date = datetime.now(),
                            is_sold = False)
            auction.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            print(form.errors)
            return HttpResponse(form.errors)
    else:
        print("yes")
        return render(request, "auctions/create.html")   


def bad_bid_error(request, auction_id):
    context = {}
    price = Auction.objects.filter(id=auction_id)[0].min_price
    context["message"] = "You have to bid at least US $" + str(price)
    context["auction_id"] = auction_id
    return render(request, "auctions/error.html", context)


def auction(request, auction_id):
    context = get_auction_context(request, auction_id)
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

    return HttpResponseRedirect(reverse("auctions:auction", kwargs={'auction_id':auction_id}))


def add_comment(request, auction_id):
    context = get_auction_context(request, auction_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        print("e valid")
        comment = Comment(
            user = context["user"],
            title = form.cleaned_data["title"],
            content = form.cleaned_data["content"],
            auction = context["details"],
            min_price = context["min_price"]
            )
        comment.save()
        context["details"].comments.add(comment)
    else:
        return HttpResponse(form.errors)
    return HttpResponseRedirect(reverse("auctions:auction", kwargs={'auction_id':auction_id}))


def bid_auction(request, auction_id):
    context = get_auction_context(request, auction_id)
    form = BidForm(request.POST)

    if form.is_valid() and form.cleaned_data["price"] >= context["min_price"]:
        bid = Bid(
            price = form.cleaned_data["price"],
            auctuion = context["details"],
            user = context["user"]
        )
        bid.save()
        context["details"].bids.add(bid)
    else:
        print("no")
        context["message"] = "Invalid price!"
        return HttpResponseRedirect(reverse("auctions:bad_bid_error", kwargs={'auction_id':auction_id}))


    return HttpResponseRedirect(reverse("auctions:auction", kwargs={'auction_id':auction_id}))


def sell_auction(request, auction_id):
    context = get_auction_context(request, auction_id)
    auction_details = Auction.objects.get(id=auction_id)
    setattr(auction_details, "is_sold", True)
    setattr(auction_details, "winner", context["winner"])
    auction_details.save()
    return HttpResponseRedirect(reverse("auctions:auction", kwargs={'auction_id':auction_id}))









