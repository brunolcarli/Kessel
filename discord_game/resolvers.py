"""
Módulo para resolução de consultas graphql.
"""
from discord_game.models import Area, Zone, Item, Profile
from kessel.utils import validate_global_id

class Resolver:

    def get_profiles(**kwargs):
        return Profile.objects.filter(**kwargs)

    def get_items(**kwargs):
        return Item.objects.filter(**kwargs)

    def get_zones(**kwargs):
        return Zone.objects.filter(**kwargs)

    def get_areas(**kwargs):
        if kwargs:
            return Area.objects.filter(zone__in=Zone.objects.filter(**kwargs))
        return Area.objects.all()
