r"""
Módulo para definição dos bjetos graphql.
Objetos, Query (consultas) e Mutations.

╦╔═┌─┐┌─┐┌─┐┌─┐┬    ╔═╗╔═╗╦
╠╩╗├┤ └─┐└─┐├┤ │    ╠═╣╠═╝║
╩ ╩└─┘└─┘└─┘└─┘┴─┘  ╩ ╩╩  ╩
"""
import graphene
from django.db.utils import IntegrityError
from discord_game.models import Profile, Item, Zone, Area, CarryItem
from discord_game.resolvers import Resolver
from kessel.settings.common import __version__


class ProfileType(graphene.ObjectType):
    """
    Define um serializador GraphQL para o objeto Profile.
    """
    discord_id = graphene.String()
    exp_earned = graphene.Int()
    is_dead = graphene.Boolean()
    life = graphene.Int()
    bag = graphene.relay.ConnectionField('discord_game.schema.CarryItemConnection')
    actual_position = graphene.List(graphene.Int)
    actual_zone = graphene.Field('discord_game.schema.ZoneType')
    actual_area = graphene.Field('discord_game.schema.AreaType')

    def resolve_actual_position(self, info, **kwargs):
        if self.actual_x_position and self.actual_y_position:
            return [self.actual_x_position, self.actual_y_position]
        return None

    def resolve_actual_zone(self, info, **kwargs):
        return self.actual_zone

    def resolve_actual_area(self, info, **kwargs):
        return self.actual_area

    def resolve_bag(self, info, **kwargs):
        return self.bag.all()

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


class CarryItemType(graphene.ObjectType):
    """
    Define a quantia de itens de um mesmo tipo que o jogador
    carrega na bolsa
    """
    item = graphene.Field(ItemType)
    stock = graphene.Int()

    def resolve_item(self, info, **kwargs):
        return self.item

    class Meta:
        interfaces = (graphene.relay.Node, )


class CarryItemConnection(graphene.relay.Connection):
    class Meta:
        node = CarryItemType

class AreaType(graphene.ObjectType):
    """
    Define um serializador graphql para o objeto Area
    """
    area_reference = graphene.String()
    area_row_max_size = graphene.Int()
    area_column_max_size = graphene.Int()

    class Meta:
        interfaces = (graphene.relay.Node,)


class AreaConnection(graphene.relay.Connection):
    class Meta:
        node = AreaType


class ZoneType(graphene.ObjectType):
    """
    Define um serializador para o objeto Zona
    """
    zone_reference = graphene.String()
    areas = graphene.relay.ConnectionField(AreaConnection)

    def resolve_areas(self, info, **kwargs):
        return self.areas.all()

    class Meta:
        interfaces = (graphene.relay.Node,)


class ZoneConnection(graphene.relay.Connection):
    class Meta:
        node = ZoneType


##################################################
# QUERY
##################################################
class Query(object):
    """
    Consultas da API.
    """
    node = graphene.relay.Node.Field()

    api_version = graphene.String(description='Returns the API actual version')
    def resolve_api_version(self, info, **kwargs):
        return __version__

    profiles = graphene.relay.ConnectionField(
        ProfileConnection,
        discord_id=graphene.String(),
        is_dead=graphene.Boolean(),
    )
    def resolve_profiles(self, info, **kwargs):
        return Resolver.get_profiles(**kwargs)

    items = graphene.relay.ConnectionField(
        ItemConnection,
        name=graphene.String()
    )
    def resolve_items(self, info, **kwargs):
        return Resolver.get_items(**kwargs)

    zones = graphene.relay.ConnectionField(
        ZoneConnection,
        zone_reference__icontains=graphene.String()
    )
    def resolve_zones(self, info, **kwargs):
        return Resolver.get_zones(**kwargs)

    areas = graphene.relay.ConnectionField(
        AreaConnection,
        zone_reference__icontains=graphene.String()
    )
    def resolve_areas(self, info, **kwargs):
        return Resolver.get_areas(**kwargs)


##################################################
# Mutation
##################################################
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


class AddItemToBag(graphene.relay.ClientIDMutation):
    """
    Adiciona um item na bolsa de um jogador.
    """
    profile = graphene.Field(ProfileType)

    class Input:
        discord_id = graphene.String(required=True)
        item_name = graphene.String(required=True)
        qt = graphene.Int()

    def mutate_and_get_payload(self, info, **_input):
        qt = _input.get('qt', 1)
        try:
            profile = Profile.objects.get(discord_id=_input.get('discord_id'))
        except Profile.DoesNotExist:
            raise Exception('Profile fornecido não encontrado')

        try:
            item = Item.objects.get(name=_input.get('item_name'))
        except Item.DoesNotExist:
            raise Exception('Item fornecido não encontrado')

        if not profile.bag.filter(item=item):
            looted = CarryItem.objects.create(item=item, stock=qt)
            looted.save()
            profile.bag.add(looted)
            profile.save()

        else:
            looted = profile.bag.get(item=item)
            looted.stock += qt
            looted.save()

        return AddItemToBag(profile)


class RemoveItemFromBag(graphene.relay.ClientIDMutation):
    """
    Remove um item da bolsa de um jogador
    """
    profile = graphene.Field(ProfileType)

    class Input:
        discord_id = graphene.String(required=True)
        item_name = graphene.String(required=True)
        qt = graphene.Int()

    def mutate_and_get_payload(self, info, **_input):
        qt = _input.get('qt', 1)
        try:
            profile = Profile.objects.get(discord_id=_input.get('discord_id'))
        except Profile.DoesNotExist:
            raise Exception('Profile fornecido não encontrado')

        try:
            item = Item.objects.get(name=_input.get('item_name'))
        except Item.DoesNotExist:
            raise Exception('Item fornecido não encontrado')

        if not profile.bag.filter(item=item):
            raise Exception('Este jogador não possui este item')

        looted = profile.bag.get(item=item)
        looted.stock -= qt
        looted.save()
        if looted.stock <= 0:
            looted.delete()

        return RemoveItemFromBag(profile)


class Mutation(object):
    profile_register = ProfileRegister.Field()
    add_item_to_bag = AddItemToBag.Field()
    remove_item_from_bag = RemoveItemFromBag.Field()
