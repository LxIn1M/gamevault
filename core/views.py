import os
import requests

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LibraryEntryUpdateForm
from .models import Game, LibraryEntry


@login_required
def home(request):
    status = request.GET.get("status", "")
    entries = LibraryEntry.objects.filter(
        user=request.user
    ).select_related("game")

    if status in LibraryEntry.Status.values:
        entries = entries.filter(status=status)

    all_entries = LibraryEntry.objects.filter(
        user=request.user
    ).select_related("game")

    stats = {
        "games_count": all_entries.count(),
        "completed_count": all_entries.filter(
            status=LibraryEntry.Status.COMPLETED
        ).count(),
        "total_hours": sum(entry.hours for entry in all_entries),
    }

    continue_entries = all_entries.filter(
        status=LibraryEntry.Status.PLAYING
    )[:8]

    return render(
        request,
        "core/home.html",
        {
            "entries": entries,
            "continue_entries": continue_entries,
            "active_status": status,
            **stats,
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(
        LibraryEntry,
        id=entry_id,
        user=request.user,
    )

    if request.method == "POST":
        form = LibraryEntryUpdateForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = LibraryEntryUpdateForm(instance=entry)

    return render(
        request,
        "core/edit_entry.html",
        {"form": form, "entry": entry},
    )


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(
        LibraryEntry,
        id=entry_id,
        user=request.user,
    )

    if request.method == "POST":
        entry.delete()
        return redirect("home")

    return render(
        request,
        "core/delete_entry.html",
        {"entry": entry},
    )


@login_required
def search_games(request):
    query = request.GET.get("q", "").strip()
    games = []
    api_error = None

    library_rawg_ids = set(
        LibraryEntry.objects.filter(
            user=request.user,
            game__rawg_id__isnull=False,
        ).values_list("game__rawg_id", flat=True)
    )

    if query:
        api_key = os.getenv("RAWG_API_KEY")

        if not api_key:
            api_error = "RAWG API key is missing. Add RAWG_API_KEY to your .env file."
        else:
            try:
                response = requests.get(
                    "https://api.rawg.io/api/games",
                    params={
                        "key": api_key,
                        "search": query,
                        "page_size": 12,
                    },
                    timeout=10,
                )
                response.raise_for_status()
                games = response.json().get("results", [])
            except requests.RequestException:
                api_error = "RAWG is unavailable right now. Try again later."

    return render(
        request,
        "core/search_games.html",
        {
            "query": query,
            "games": games,
            "library_rawg_ids": library_rawg_ids,
            "api_error": api_error,
        },
    )


@login_required
def add_rawg_game(request, rawg_id):
    if request.method != "POST":
        return redirect("search_games")

    api_key = os.getenv("RAWG_API_KEY")
    if not api_key:
        return redirect("search_games")

    try:
        response = requests.get(
            f"https://api.rawg.io/api/games/{rawg_id}",
            params={"key": api_key},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException:
        return redirect("search_games")

    data = response.json()

    game, _ = Game.objects.get_or_create(
        rawg_id=rawg_id,
        defaults={
            "title": data["name"],
            "released": data.get("released"),
            "background_image": data.get("background_image"),
        },
    )

    entry, _ = LibraryEntry.objects.get_or_create(
        user=request.user,
        game=game,
    )

    return redirect("edit_entry", entry_id=entry.id)
