from django import forms
from .models import LibraryEntry

class LibraryEntryUpdateForm(forms.ModelForm):
    class Meta:
        model = LibraryEntry
        fields = ["status", "hours", "rating"]

    def clean_hours(self):
        hours = self.cleaned_data["hours"]

        if hours < 0:
            raise forms.ValidationError("Hours cannot be negative.")

        return hours

    def clean_rating(self):
        rating = self.cleaned_data["rating"]

        if rating is not None and not 0 <= rating <= 10:
            raise forms.ValidationError("Rating must be between 0 and 10.")

        return rating