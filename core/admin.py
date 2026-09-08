from django.contrib import admin
from .models import Game, LibraryEntry

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    
@admin.register(LibraryEntry)
class LibraryEntryAdmin(admin.ModelAdmin):
    list_display = ("game_title", "status", "hours", "rating")

    def game_title(self, obj):
        return obj.game.title