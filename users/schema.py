import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()           # regiter new user
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()          # login
    update_account = mutations.UpdateAccount.Field()            # update
    resend_activation_email = mutations.ResendActivationEmail.Field()       # resend mail
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()       # reset password
    password_reset = mutations.PasswordReset.Field()        #reset passwrd

class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation =Mutation)