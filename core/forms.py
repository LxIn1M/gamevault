from django import forms

from .models import LibraryEntry


class LibraryEntryForm(forms.ModelForm):
    class Meta:
        model = LibraryEntry
        fields = ["game", "status", "hours", "rating"]

class LibraryEntryUpdateForm(forms.ModelForm):
    class Meta:
        model = LibraryEntry
        fields = ["status", "hours", "rating"]