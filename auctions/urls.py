from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newitem", views.new_item, name="new_item"),
    path("item/<int:idx>",views.viewitem, name="item"),
    path("watchlist/<int:idx>",views.addwatchlist,name="addwatchlist"),
    path("user/watchlist",views.watchlist,name="watchlist"),
    path("item/<int:idx>/close",views.closebid,name="closebid"),
    path("item/<int:idx>/comment",views.comment,name="comment"),
    path("categories",views.viewcategories,name="categories"),
    path("categories/<int:id>", views.categorieslist, name="categorieslist"),
]
