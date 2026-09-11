import os

import requests

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    LibraryEntryUpdateForm,
    SteamConnectForm,
)
from .models import (
    Game,
    LibraryEntry,
    SteamProfile,
)
from .services.steam import (
    SteamAPIError,
    get_owned_games,
    get_player_summary,
    get_steam_header_image,
)


@login_required
def home(request):
    status = request.GET.get("status", "")

    entries = (
        LibraryEntry.objects
        .filter(user=request.user)
        .select_related("game")
    )

    if status in LibraryEntry.Status.values:
        entries = entries.filter(status=status)

    all_entries = (
        LibraryEntry.objects
        .filter(user=request.user)
        .select_related("game")
    )

    stats = all_entries.aggregate(
        total_hours=Sum("hours"),
    )

    games_count = all_entries.count()

    completed_count = all_entries.filter(
        status=LibraryEntry.Status.COMPLETED
    ).count()

    total_hours = round(
        stats["total_hours"] or 0,
        1,
    )

    continue_entries = all_entries.filter(
        status=LibraryEntry.Status.PLAYING
    )[:8]

    try:
        steam_profile = request.user.steam_profile
    except SteamProfile.DoesNotExist:
        steam_profile = None

    steam_form = SteamConnectForm()

    return render(
        request,
        "core/home.html",
        {
            "entries": entries,
            "continue_entries": continue_entries,
            "active_status": status,
            "games_count": games_count,
            "completed_count": completed_count,
            "total_hours": total_hours,
            "steam_profile": steam_profile,
            "steam_form": steam_form,
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("home")

    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(
        LibraryEntry,
        id=entry_id,
        user=request.user,
    )

    if request.method == "POST":
        form = LibraryEntryUpdateForm(
            request.POST,
            instance=entry,
        )

        if form.is_valid():
            form.save()

            return redirect("home")

    else:
        form = LibraryEntryUpdateForm(
            instance=entry,
        )

    return render(
        request,
        "core/edit_entry.html",
        {
            "form": form,
            "entry": entry,
        },
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
        {
            "entry": entry,
        },
    )


@login_required
def search_games(request):
    query = request.GET.get("q", "").strip()

    games = []

    error = None

    library_rawg_ids = set(
        LibraryEntry.objects
        .filter(
            user=request.user,
            game__rawg_id__isnull=False,
        )
        .values_list(
            "game__rawg_id",
            flat=True,
        )
    )

    if query:
        rawg_api_key = os.getenv("RAWG_API_KEY")

        if not rawg_api_key:
            error = (
                "RAWG_API_KEY is missing "
                "from the .env file."
            )

        else:
            try:
                response = requests.get(
                    "https://api.rawg.io/api/games",
                    params={
                        "key": rawg_api_key,
                        "search": query,
                        "page_size": 20,
                    },
                    timeout=10,
                )

                response.raise_for_status()

                data = response.json()

                games = data.get("results", [])

            except requests.RequestException:
                error = (
                    "Could not connect to RAWG."
                )

    return render(
        request,
        "core/search_games.html",
        {
            "games": games,
            "query": query,
            "error": error,
            "library_rawg_ids": library_rawg_ids,
        },
    )


@login_required
@require_POST
def add_rawg_game(request, rawg_id):
    rawg_api_key = os.getenv("RAWG_API_KEY")

    if not rawg_api_key:
        messages.error(
            request,
            "RAWG API key is missing.",
        )

        return redirect("search_games")

    try:
        response = requests.get(
            f"https://api.rawg.io/api/games/{rawg_id}",
            params={
                "key": rawg_api_key,
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException:
        messages.error(
            request,
            "Could not retrieve game from RAWG.",
        )

        return redirect("search_games")

    game, _ = Game.objects.get_or_create(
        rawg_id=rawg_id,
        defaults={
            "title": data.get(
                "name",
                "Unknown game",
            ),
            "released": data.get("released") or None,
            "background_image": (
                data.get("background_image") or ""
            ),
        },
    )

    entry, created = LibraryEntry.objects.get_or_create(
        user=request.user,
        game=game,
    )

    if not created:
        messages.info(
            request,
            "This game is already in your library.",
        )

    return redirect(
        "edit_entry",
        entry_id=entry.id,
    )


@login_required
@require_POST
def connect_steam(request):
    form = SteamConnectForm(request.POST)

    if not form.is_valid():
        messages.error(
            request,
            "Enter a valid SteamID64.",
        )

        return redirect("home")

    steam_id = form.cleaned_data["steam_id"]

    try:
        player = get_player_summary(steam_id)

    except SteamAPIError as error:
        messages.error(
            request,
            str(error),
        )

        return redirect("home")

    existing_profile = SteamProfile.objects.filter(
        steam_id=steam_id
    ).exclude(
        user=request.user
    ).exists()

    if existing_profile:
        messages.error(
            request,
            "This Steam account is already connected "
            "to another LixDex account.",
        )

        return redirect("home")

    SteamProfile.objects.update_or_create(
        user=request.user,
        defaults={
            "steam_id": steam_id,
            "persona_name": player.get(
                "personaname",
                "",
            ),
            "avatar_url": player.get(
                "avatarfull",
                "",
            ),
            "profile_url": player.get(
                "profileurl",
                "",
            ),
        },
    )

    messages.success(
        request,
        "Steam account connected.",
    )

    return redirect("home")


@login_required
@require_POST
def sync_steam(request):
    try:
        steam_profile = request.user.steam_profile

    except SteamProfile.DoesNotExist:
        messages.error(
            request,
            "Connect your Steam account first.",
        )

        return redirect("home")

    try:
        steam_games = get_owned_games(
            steam_profile.steam_id
        )

        player = get_player_summary(
            steam_profile.steam_id
        )

    except SteamAPIError as error:
        messages.error(
            request,
            str(error),
        )

        return redirect("home")

    added_games = 0
    updated_games = 0

    with transaction.atomic():
        for steam_game in steam_games:
            app_id = steam_game.get("appid")
            title = steam_game.get("name")

            if not app_id or not title:
                continue

            playtime_minutes = int(
                steam_game.get(
                    "playtime_forever",
                    0,
                )
            )

            game = Game.objects.filter(
                steam_app_id=app_id
            ).first()

            # Try to merge with a game previously added
            # from RAWG instead of creating a duplicate.
            if game is None:
                game = (
                    Game.objects
                    .filter(
                        title__iexact=title,
                        steam_app_id__isnull=True,
                    )
                    .first()
                )

            if game is None:
                game = Game.objects.create(
                    steam_app_id=app_id,
                    title=title,
                    background_image=(
                        get_steam_header_image(
                            app_id
                        )
                    ),
                )

            else:
                changed = False

                if game.steam_app_id is None:
                    game.steam_app_id = app_id
                    changed = True

                if not game.background_image:
                    game.background_image = (
                        get_steam_header_image(
                            app_id
                        )
                    )
                    changed = True

                if changed:
                    game.save()

            entry, created = (
                LibraryEntry.objects.get_or_create(
                    user=request.user,
                    game=game,
                )
            )

            entry.steam_playtime_minutes = (
                playtime_minutes
            )

            entry.hours = round(
                playtime_minutes / 60,
                1,
            )

            entry.save(
                update_fields=[
                    "steam_playtime_minutes",
                    "hours",
                ]
            )

            if created:
                added_games += 1

            else:
                updated_games += 1

        steam_profile.persona_name = player.get(
            "personaname",
            steam_profile.persona_name,
        )

        steam_profile.avatar_url = player.get(
            "avatarfull",
            steam_profile.avatar_url,
        )

        steam_profile.profile_url = player.get(
            "profileurl",
            steam_profile.profile_url,
        )

        steam_profile.last_synced_at = timezone.now()

        steam_profile.save()

    messages.success(
        request,
        (
            f"Steam synchronized. "
            f"{added_games} games added, "
            f"{updated_games} games updated."
        ),
    )

    return redirect("home")


@login_required
@require_POST
def disconnect_steam(request):
    SteamProfile.objects.filter(
        user=request.user
    ).delete()

    messages.success(
        request,
        "Steam account disconnected.",
    )

    return redirect("home")