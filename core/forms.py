from django import forms

from .models import LibraryEntry


class LibraryEntryForm(forms.ModelForm):
    class Meta:
        model = LibraryEntry
        fields = ["game", "status", "hours", "rating"]