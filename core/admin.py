from django.contrib import admin
from .models import Game, LibraryEntry


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "rawg_id",
        "title",
        "released",
    )


@admin.register(LibraryEntry)
class LibraryEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "game",
        "status",
        "hours",
        "rating",
    )