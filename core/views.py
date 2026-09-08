from django.shortcuts import render
from .models import LibraryEntry
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .forms import LibraryEntryForm

@login_required
def home(request):
    entries = LibraryEntry.objects.filter(user=request.user)

    context = {
        "username": request.user.username,
        "games_count": entries.count(),
        "entries": entries,
    }

    return render(request, "core/home.html", context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})

@login_required
def add_game(request):
    if request.method == "POST":
        form = LibraryEntryForm(request.POST)

        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()

            return redirect("home")
    else:
        form = LibraryEntryForm()

    return render(request, "core/add_game.html", {"form": form})
