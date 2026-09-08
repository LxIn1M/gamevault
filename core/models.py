from django.db import models
from django.conf import settings


class Game(models.Model):
    title = models.CharField(max_length=100)
    
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
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.BACKLOG,
    )
    hours = models.IntegerField(default=0)
    rating = models.FloatField(null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game"],
                name="unique_user_game",
            )
        ]
    
    def __str__(self):
        return f"{self.game.title} - User: {self.user} - Status: {self.get_status_display()} - Hours: {self.hours} - Rating: {self.rating}"
    
