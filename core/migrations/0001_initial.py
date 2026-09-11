from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rawg_id", models.IntegerField(blank=True, null=True, unique=True)),
                ("title", models.CharField(max_length=200)),
                ("released", models.DateField(blank=True, null=True)),
                ("background_image", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="LibraryEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(
                    choices=[
                        ("playing", "Playing"),
                        ("completed", "Completed"),
                        ("backlog", "Backlog"),
                        ("dropped", "Dropped"),
                    ],
                    default="backlog",
                    max_length=20,
                )),
                ("hours", models.IntegerField(default=0)),
                ("rating", models.FloatField(blank=True, null=True)),
                ("game", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.game")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name="libraryentry",
            constraint=models.UniqueConstraint(fields=("user", "game"), name="unique_user_game"),
        ),
    ]
