from django.urls import path
from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("bad_bid_error/<int:auction_id>", views.bad_bid_error, name="bad_bid_error"),
    path("add_to_watchlist/<int:auction_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("add_comment/<int:auction_id>", views.add_comment, name="add_comment"),
    path("bid_auction/<int:auction_id>", views.bid_auction, name="bid_auction"),
    path("sell_auction/<int:auction_id>", views.sell_auction, name="sell_auction"),
    path("category/<str:category_id>", views.category, name="category"),
]
