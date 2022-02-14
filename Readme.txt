1) Building a custom user model
        as we want to capture information about the user such as their name, email, etc so we can log them in;
        now django bydefault has this model available that we can build for a user; but generally what we want to do is, we want to extend it using "AbstractUser" or we want to completely override it using "AbstractBaseUser" (allow us to build from scratch) and make our own model.
        ( AbstractUser helps us to add new fields within the pre-built user model of Django. If you want to learn more about AbstractUser )
        we have used the AbstractUser to extend upon the user fields

                * we can define what we want the user to utilize as the kind of the USERNAME_FIELD and EMAIL_FIELD
                * as by utilizing the fields now we need to register this custom table

                                AUTH_USER_MODEL = 'users.ExtendUser'  (in settings.py)

                * makemigrations and migrate bcoz it allows us to actually build the table

        register your model at admin.py

2) setup GraphQL and JWT (JSON web tokens)

        install the graphene-django package, it allows us to utilize graph in our django application
                                pip install graphene-django

        install django-graphql-jwt package, it allow us to work with jwt with graph; JSON Web Token, is an open standard used to share security information between two parties — a client and a server. Each JWT contains encoded JSON objects, including a set of claims. JWTs are signed using a cryptographic algorithm to ensure that the claims cannot be altered after the token is issued.

                                pip install django-graphql-jwt      ( follow up the documentation for sucessfull installation of this package "https://pypi.org/project/django-graphql-jwt/")


        add the following packages into your INSTALLED_APPS
                               * 'graphene_django'
                               * 'graphql_jwt.refresh_token.apps.RefreshTokenConfig'   (refresh tokens allow us the users to activate or collect a new token if they haven't been logged in for some time potentially)



        Add AuthenticationMiddleware middleware to your MIDDLEWARE settings:

                                MIDDLEWARE = [
                                       "django.contrib.auth.middleware.AuthenticationMiddleware",
                                ]

        define schema and Add JSONWebTokenMiddleware middleware to your GRAPHENE settings; ( we are telling graphene to use JWT middleware with the help of 'MIDDLEWARE' option ):
                                GRAPHENE = {
                                    'SCHEMA' : 'users.schema.schema',
                                        "MIDDLEWARE": [
                                            "graphql_jwt.middleware.JSONWebTokenMiddleware",
                                        ],
                                    S}

        Add JSONWebTokenBackend backend to your AUTHENTICATION_BACKENDS bcoz we are utilizing different authentication backend method so we need to inform django about this:

                                AUTHENTICATION_BACKENDS = [
                                    "graphql_jwt.backends.JSONWebTokenBackend",         ( allow us to utilize our tokens)
                                    "django.contrib.auth.backends.ModelBackend",
                                ]




        migrate and "Refresh tokens" will be visible on the admin site; which will show us all the tokens thats currently being utilized by any user that's logged in



3) Setup Django-GraphQL_Auth
        install django-graphql-auth in your system bcoz This library helps us with functionality like registering a new user, verifying the email address of the newly signed up user, changing the user email address, changing the user password, and many more.
                                * pip install django-graphql-auth

        the above step will also install all the required dependencies we required such as django-filter and auth, add the dependencies in your INSTALLED_APPS
                                * 'graphql_auth',
                                * 'django_filters',                 (Django-filter provides a simple way to filter down a queryset based on parameters a user provides.)

        update the AUTHENTICATION_BACKENDS

                            AUTHENTICATION_BACKENDS = [
                                    # "graphql_jwt.backends.JSONWebTokenBackend",
                                    'graphql_auth.backends.GraphQLAuthBackend',             ( it is provided by graphql-auth )
                                    "django.contrib.auth.backends.ModelBackend",
                            ]

                         ( we are gonna utilize this new package which is essentially just a wrapper around all the other applications we've installed and its gonna manage those seamlessly so that we're not writing extraordinary amount of code in order to achieve what we want to achieve )

        migrate (because this is going to add few different tables


        register your model at admin.py


        now we need to bring in the model of new packages we just installed (i.e. dont exist in models.py file); to do that we need to register model based upon the INSTALLED_APPLICATION
                          * import apps using "from django.apps import apps"

                          *  " app = apps.get_app_config('graphql_auth') "    (in our  setting we have registered our application i.e. 'graphql_auth' so through this query we are grabbing the models of graphql_auth and storing them in 'app' variable

                          *   register models of app

                                    ( now we have User status in our admin page )

                          * import csrf_exempt ( allow us to basically telling the urls that it doesn't need the token. This is a security exemption that you should take seriously. )
                                        from django.views.decorators.csrf import csrf_exempt

                          * import GraphQLView
                                        from graphene_django.views import GraphQLView

                          * set the path
                                           path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))

        create a schema file and build schema
                            * import graphene
                            * create a Query class with "UserQuery" and "MeQuery"
                                        GraphQL Auth provides the "UserQuery" (to query users with some useful filters) and "MeQuery" (to retrieve data for the currently authenticated user); import them




        build schema i.e. "schema = graphene.Schema(query=Query)"

4) User Registration

        




