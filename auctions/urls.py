from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("add_to_watchlist/<int:auction_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("add_comment/<int:auction_id>", views.add_comment, name="add_comment")
]
