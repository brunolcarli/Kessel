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
    life = models.IntegerField(default=100)
    is_dead = models.BooleanField(default=False)
    bag = models.ManyToManyField('discord_game.Item')
    actual_x_position = models.IntegerField(null=True, default=None)
    actual_y_position = models.IntegerField(null=True, default=None)
    actual_zone = models.ForeignKey(
        'discord_game.Zone',
        on_delete=models.CASCADE,
        null=True
    )
    actual_area = models.ForeignKey(
        'discord_game.Area',
        on_delete=models.CASCADE,
        null=True
    )


class Item(models.Model):
    """
    Define as caracteristicas de um item do jogo.
    """
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)
    description = models.TextField(blank=True, null=True)


class Area(models.Model):
    """
    Define uma área pertencente à uma determinada Zona de exploração
    """
    area_reference = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True
    )
    area_row_max_size = models.IntegerField(default=1)
    area_column_max_size = models.IntegerField(default=1)


class Zone(models.Model):
    """
    Define as caracteristicas de uma Zona de exploração
    """
    zone_reference = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True
    )
    areas = models.ManyToManyField(Area)
