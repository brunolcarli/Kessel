import graphene
from kessel.settings.common import __version__


class Query(object):
    api_version = graphene.String()
    def resolve_api_version(self, info, **kwargs):
        return __version__


class Mutation(object):
    """
    Main mutations
    """
