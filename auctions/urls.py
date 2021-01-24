from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.new_listing, name="new_listing"),
    path("title", views.auctionpage, name="auctionpage"),
    path("Mywatchlist", views.watchlist, name="watchlist"),
    path("delete", views.delete, name="delete"),
    path("comment", views.comment, name="comment"),
    path("closeaution", views.close, name="close"),
    path("Tags", views.tags, name="tags"),
]
