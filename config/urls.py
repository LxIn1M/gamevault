from django.contrib import admin
from django.urls import include, path

from core.views import (
    home,
    register,
    edit_entry,
    delete_entry,
    search_games,
    add_rawg_game,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("entry/<int:entry_id>/edit/", edit_entry, name="edit_entry"),
    path("entry/<int:entry_id>/delete/", delete_entry, name="delete_entry"),
    path("search/", search_games, name="search_games"),
    path("games/<int:rawg_id>/add/", add_rawg_game, name="add_rawg_game"),
]
