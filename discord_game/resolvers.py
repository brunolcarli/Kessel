"""
Módulo para resolução de consultas graphql.
"""
from discord_game.models import Area, Zone, Item, Profile
from kessel.utils import validate_global_id

class Resolver:

    def get_profiles(**kwargs):
        return Profile.objects.filter(**kwargs)
