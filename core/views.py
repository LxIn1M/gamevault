from django.shortcuts import render
from .models import LibraryEntry

def home(request):
    entries = LibraryEntry.objects.all()
    context = {
    "username": "LX",
    "games_count": entries.count(),
    "entries": entries,
}
    return render(request, "core/home.html", context)
