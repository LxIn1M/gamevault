from core import views
from django.contrib import admin
from django.urls import path, include

from core.views import home, register, add_game

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("add-game/", add_game, name="add_game"),
]
