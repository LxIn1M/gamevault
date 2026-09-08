from django.db import models


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

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.BACKLOG,
    )
    hours = models.IntegerField(default=0)
    rating = models.FloatField(null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.game.title} - Status: {self.get_status_display()} - Hours: {self.hours} - Rating: {self.rating}"