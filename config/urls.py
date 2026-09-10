from core import views
from django.contrib import admin
from django.urls import path, include

from core.views import home, register, add_game, edit_entry, delete_entry

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("add-game/", add_game, name="add_game"),
    path("entry/<int:entry_id>/edit/", edit_entry, name="edit_entry"),
    path("entry/<int:entry_id>/delete/", delete_entry, name="delete_entry"),
]
