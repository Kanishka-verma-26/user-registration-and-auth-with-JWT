1) Building a custom user model
        as we want to capture infoormation about the user such as their name, email, etc so we can log them in;
        now django bydefault has this model available that we can build for a user; but generally what we want to do is, we want to extend it using "AbstractUser" or we want to completely override it using "AbstractBaseUser" (allow us to build from scratch) and make our own model.
        we have used the AbstractUser to extend upon the user fields

                * we can define what we want the user to utilize as the kind of the USERNAME_FIELD and EMAIL_FIELD
                * as by utilizing the fields now we need to register this custom table

                                AUTH_USER_MODEL = 'users.ExtendUser'  (in settings.py)

                * makemigrations and migrate bcoz it allows us to actually build the table

        register your model at admin.py

2) setup GraphQL and JWT (JSON web tokens)

        install the graphene-django package, it allows us to utilize graph in our django application
                                pip install graphene-django

        install django-graphql-jwt package, it allow us to work with jwt with graph
                                pip install django-graphql-jwt      ( follow up the documentation for sucessfull installation of this package "https://pypi.org/project/django-graphql-jwt/")

        Add AuthenticationMiddleware middleware to your MIDDLEWARE settings:

                                MIDDLEWARE = [
                                       "django.contrib.auth.middleware.AuthenticationMiddleware",
                                ]

        define schema and Add JSONWebTokenMiddleware middleware to your GRAPHENE settings:
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



        add the following packages into your INSTALLED_APPS
                               * 'graphene_django'
                               * 'graphql_jwt.refresh_token.apps.RefreshTokenConfig'   (refresh tokens allow us the users to activate or collect a new token if they haven't been logged in for some time potentially)


        migrate and "Refresh tokens" will be visible on the admin site; which will show us all the tokens thats currently being utilized by any user that's logged in



3) Setup Django-GraphQL_Auth
        install django-graphql-auth in your system bcoz this is going to provide all the features we're going to build upon to actually build this system in our application
                                * pip install django-graphql-auth

        the above step will also install all the required dependencies we required such as django-filter and auth, add the dependencies in your INSTALLED_APPS
                                * 'graphql_auth',
                                * 'django_filters',

        update the AUTHENTICATION_BACKENDS

                            AUTHENTICATION_BACKENDS = [
                                    # "graphql_jwt.backends.JSONWebTokenBackend",
                                    'graphql_auth.backends.GraphQLAuthBackend',
                                    "django.contrib.auth.backends.ModelBackend",
                            ]

                         ( now if you want to use a JWT utilizing this off back
