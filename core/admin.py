from django.contrib import admin

from .models import (
    Game,
    LibraryEntry,
    SteamProfile,
)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "rawg_id",
        "steam_app_id",
    )

    search_fields = (
        "title",
    )


@admin.register(LibraryEntry)
class LibraryEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "game",
        "status",
        "hours",
        "steam_playtime_minutes",
        "rating",
    )

    list_select_related = (
        "user",
        "game",
    )


@admin.register(SteamProfile)
class SteamProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "steam_id",
        "persona_name",
        "last_synced_at",
    )