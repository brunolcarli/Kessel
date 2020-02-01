from django.db import models


class Profile(models.Model):
    """
    Define as caracteristicas de um usuário do sistema.
    """
    discord_id = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True
    )
    exp_earned = models.IntegerField(default=0)


class Item(models.Model):
    """
    Define as caracteristicas de um item do jogo.
    """
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)
    description = models.TextField(blank=True, null=True)
