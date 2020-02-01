import graphene
from django.db.utils import IntegrityError
from discord_game.models import Profile, Item
from kessel.settings.common import __version__


class ProfileType(graphene.ObjectType):
    """
    Define um serializador GraphQL para o objeto Profile.
    """
    discord_id = graphene.String()
    exp_earned = graphene.Int()

    class Meta:
        interfaces = (graphene.relay.Node,)


class ProfileConnection(graphene.relay.Connection):
    class Meta:
        node = ProfileType


class ItemType(graphene.ObjectType):
    """
    Define um serializador GraphQL para o objeto Item.
    """
    name = graphene.String()
    description = graphene.String()

    class Meta:
        interfaces = (graphene.relay.Node,)


class ItemConnection(graphene.relay.Connection):
    class Meta:
        node = ItemType


class Query(object):
    """
    Consultas da API.
    """
    node = graphene.relay.Node.Field()

    api_version = graphene.String(description='Returns the API actual version')
    def resolve_api_version(self, info, **kwargs):
        return __version__

    profiles = graphene.relay.ConnectionField(ProfileConnection)
    def resolve_profiles(self, info, **kwarg):
        return Profile.objects.all()

    items = graphene.relay.ConnectionField(ItemConnection)
    def resolve_items(self, info, **kwarg):
        return Item.objects.all()


class ProfileRegister(graphene.relay.ClientIDMutation):
    """
    Registra o profile de um usuário no sistema.
    """
    profile = graphene.Field(ProfileType)

    class Input:
        discord_id = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **_input):
        discord_id = _input.get('discord_id')

        try:
            profile = Profile.objects.create(discord_id=discord_id)
        except IntegrityError:
            raise Exception('Profile já registrado.')

        return ProfileRegister(profile)


class Mutation(object):
    profile_register = ProfileRegister.Field()
