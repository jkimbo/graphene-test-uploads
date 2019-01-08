from graphene import ObjectType, Schema
from graphql_jwt import ObtainJSONWebToken, Refresh, Verify

from app.schema import AppMutation

class Mutation(ObjectType, AppMutation):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()

ROOT_SCHEMA = Schema(mutation=Mutation)
