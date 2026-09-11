from django import forms

from .models import LibraryEntry


class LibraryEntryUpdateForm(forms.ModelForm):
    class Meta:
        model = LibraryEntry
        fields = ["status", "hours", "rating"]

    def clean_hours(self):
        hours = self.cleaned_data["hours"]

        if hours < 0:
            raise forms.ValidationError(
                "Hours cannot be negative."
            )

        return hours

    def clean_rating(self):
        rating = self.cleaned_data["rating"]

        if rating is not None and not 0 <= rating <= 10:
            raise forms.ValidationError(
                "Rating must be between 0 and 10."
            )

        return rating


class SteamConnectForm(forms.Form):
    steam_id = forms.CharField(
        max_length=20,
        label="SteamID64",
        widget=forms.TextInput(
            attrs={
                "placeholder": "7656119XXXXXXXXXX",
                "autocomplete": "off",
            }
        ),
    )

    def clean_steam_id(self):
        steam_id = self.cleaned_data["steam_id"].strip()

        if not steam_id.isdigit():
            raise forms.ValidationError(
                "SteamID must contain only numbers."
            )

        if len(steam_id) != 17:
            raise forms.ValidationError(
                "SteamID64 should contain 17 digits."
            )

        return steam_id