from django.conf import settings
from django.db import models


class Game(models.Model):
    rawg_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
    )

    steam_app_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)

    released = models.DateField(
        null=True,
        blank=True,
    )

    background_image = models.URLField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class LibraryEntry(models.Model):
    class Status(models.TextChoices):
        PLAYING = "playing", "Playing"
        COMPLETED = "completed", "Completed"
        BACKLOG = "backlog", "Backlog"
        DROPPED = "dropped", "Dropped"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.BACKLOG,
    )

    # FloatField allows e.g. 123.4 hours instead of only whole hours.
    hours = models.FloatField(default=0)

    # Exact value received from Steam.
    steam_playtime_minutes = models.PositiveIntegerField(default=0)

    rating = models.FloatField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game"],
                name="unique_user_game",
            )
        ]

    def __str__(self):
        return (
            f"{self.game.title} - "
            f"Status: {self.get_status_display()} - "
            f"Hours: {self.hours} - "
            f"Rating: {self.rating}"
        )


class SteamProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="steam_profile",
    )

    steam_id = models.CharField(
        max_length=20,
        unique=True,
    )

    persona_name = models.CharField(
        max_length=200,
        blank=True,
    )

    avatar_url = models.URLField(
        blank=True,
    )

    profile_url = models.URLField(
        blank=True,
    )

    last_synced_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username} - {self.persona_name or self.steam_id}"