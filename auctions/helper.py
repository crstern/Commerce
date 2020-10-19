from django.contrib import auth
from .models import User, Auction, Bid, Comment
from .forms import CommentForm, BidForm
from pprint import pprint

def get_max_price(auction_details):
    maximum = 0
    user = None
    for bid in auction_details.bids.all():
        if bid.price > maximum:
            maximum = bid.price
            user = bid.user
    return maximum, user


def potential_winner(auction_details, user):
    price, winner = get_max_price(auction_details) 
    return winner
    

def can_bid(auction_details, user):
    if user == auction_details.author:
        return False
    return True


def get_auction_context(request, auction_id):
    auction_details = Auction.objects.filter(id=auction_id)[0]
    user = auth.get_user(request)
    context = {}
    
    if len(auction_details.bids.all()) == 0:
        context["min_price"] = auction_details.price
    else:
        context["min_price"], _ = get_max_price(auction_details)

    winner = potential_winner(auction_details, user)
    if winner and user == auction_details.author:
        context["sell_form"] = True
    else:
        context["sell_form"] = False
    
    context["is_sold"] = auction_details.is_sold
    context["auction"] = auction_id
    context["details"] = auction_details
    context["bid_form"] = BidForm()
    context["bid_form"].fields["price"].min_value = context["min_price"]
    context["user"] = user
    context["comments"] = auction_details.comments.all()
    context["comment_form"] = CommentForm()
    context["winner"] = winner
    context["can_bid"] = can_bid(auction_details, user)
    return context
