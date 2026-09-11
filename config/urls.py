from django.contrib import admin
from django.urls import include, path

from core.views import (
    add_rawg_game,
    connect_steam,
    delete_entry,
    disconnect_steam,
    edit_entry,
    home,
    register,
    search_games,
    sync_steam,
)


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "accounts/",
        include(
            "django.contrib.auth.urls"
        ),
    ),

    path(
        "",
        home,
        name="home",
    ),

    path(
        "register/",
        register,
        name="register",
    ),

    path(
        "entry/<int:entry_id>/edit/",
        edit_entry,
        name="edit_entry",
    ),

    path(
        "entry/<int:entry_id>/delete/",
        delete_entry,
        name="delete_entry",
    ),

    path(
        "search/",
        search_games,
        name="search_games",
    ),

    path(
        "games/<int:rawg_id>/add/",
        add_rawg_game,
        name="add_rawg_game",
    ),

    path(
        "steam/connect/",
        connect_steam,
        name="connect_steam",
    ),

    path(
        "steam/sync/",
        sync_steam,
        name="sync_steam",
    ),

    path(
        "steam/disconnect/",
        disconnect_steam,
        name="disconnect_steam",
    ),
]