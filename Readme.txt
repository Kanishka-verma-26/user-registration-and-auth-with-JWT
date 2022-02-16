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

                          * set the path.
                                           path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))

        create a schema file and build schema
                            * import graphene
        create a Query class with "UserQuery" and "MeQuery"
                            ( GraphQL Auth provides the "UserQuery" (to query users with some useful filters) and "MeQuery" (to retrieve data for the currently authenticated user); import them )

        build schema i.e. "schema = graphene.Schema(query=Query)"


                                        """"""
                                            import graphene
                                            from graphql_auth.schema import UserQuery, MeQuery

                                            class Query(UserQuery, MeQuery, graphene.ObjectType):
                                                    pass

                                            schema = graphene.Schema(query=Query)

                                        """"""


        # ( as you have built the query class now you can easily access the details of any user like : )
                                        """"
                                            query{
	                                            users{
                                                    edges{                      ( edges allow us to extract all the information about users or all users or collection of objects )
                                                        node{                     ( node represents the data that each edge has )
                                                            username
                                                            email
                                                        }
                                                    }
                                                }
                                            }
                                        """"

        ( as we didn't wrote anything in the Query class, so from where did this "users" come from ?; graphql_auth already has those, it bring in all those in an abstract manner by UserQuery and MeQuery

        ( we can also collect information about the user i.e. currently logged in using "MeQuery", we dont need to define edges and users in this because Me can only represnt to a particular user i.e. currently logged in)

                                        """"
                                            query{
                                                me{
                                                    username
                                                }
                                            }
                                        """"


4) User Registration

        we have seen in many platforms that after registration the user gets a confirmation email to click some link or button and get registered into a platform; to achieve this define the below LOC in settings.py file

                                "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'"              (this will send the email to the console)

        set up the mutations in to the schema file to register a user    ( mutations allow us to add data from frontend )

                                * import mutations from graphql_auth
                                * set up a mutation class (lets say AuthMutation) and add below code, it will allow a user to get registered.
                                                register = mutations.Register.Field()

                                * set up a new mutation class by passing the previous mutation class (AuthMutation) bcoz AuthMutation is going to pass new data fields and we need to utilize those fields into the table
                                * extend  your schema to utilize new mutation


                                                    """"""
                                                          import graphene
                                                          from graphql_auth import mutations
                                                          from graphql_auth.schema import UserQuery, MeQuery

                                                          class AuthMutation(graphene.ObjectType):
                                                                    register = mutations.Register.Field()           # regiter new user


                                                          class Query(UserQuery, MeQuery, graphene.ObjectType):
                                                                    pass

                                                          class Mutation(AuthMutation,graphene.ObjectType):
                                                                    pass

                                                          schema = graphene.Schema(query=Query,mutation =Mutation)
                                                    """"""


       connect your graphql to JWT to register a user ; add below code in settings.py file:

                                ******
                                        GRAPHQL_JWT ={
                                                "JWT_ALLOW_ANY_CLASSES": [
                                                        "graphql_auth.mutations.Register",
                                                ],
                                                "JWT_VERIFY_EXPIRATION": True,                      # refreshToken requirements
                                                "JWT_LONG_RUNNING_REFRESH_TOKEN": True,             # refreshToken requirements
                                        }
                                ******


       ( now we can register a user from frontend to backend with the following code )

                                ******
                                        mutation{
                                             register(
                                                 email:"<email>",
                                                 username:"<username>"
                                                 password1:"<pass1>",
                                                 password2:"<pass2>"
                                             ) {
                                                 success                                 # we want a signal from backend to tell us user was successfully registered; which can be achieved by below parameters
                                                 errors
                                                 refreshToken
                                                 token
                                             }
                                        }
                                ******


5) Account Verification

         following to the previous step (4), when we actually registered a new user we got a link (which was an email i.e. sent to the  user) in our console which is required to verify the user's account;
                ( you need to verify your account because without verification you can not login; the verified accounts will be visible in "User status" column at admin page )

                        example of link : """" <p>http://127.0.0.1:8000/activate/eyJ1c2VybmFtZSI6ImhvbmV5IiwiYWN0aW9uIjoiYWN0aXZhdGlvbiJ9:1nJrWa:iU5pg3K7PoMwijik0ch_9R7-GT3MubgEStuSdHPr4d4</p> """"



         the above link won't work directly because we haven't set the url for that ; to access this link from frontend we need to make a new path and a page
         that can handle this link (i.e. take this code and utilise it and verify the user ) to achieve that we need to set up a new mutation because we want to
         make a change in our database. add the below LOC in your first mutation class of schema file to verify user:

                            verify_account = mutations.VerifyAccount.Field()



                            """"""
                                class AuthMutation(graphene.ObjectType):
                                        register = mutations.Register.Field()           # regiter new user
                                        verify_account = mutations.VerifyAccount.Field()        # verify user
                            """"""



         now we need to define our mutation verification in GRAPHQL_JWT in settings.py

                             "graphql_auth.mutations.VerifyAccount",



                             """"""
                                    GRAPHQL_JWT ={
                                            "JWT_ALLOW_ANY_CLASSES": [
                                                    "graphql_auth.mutations.Register",
                                                     "graphql_auth.mutations.VerifyAccount",
                                            ],
                                            "JWT_VERIFY_EXPIRATION": True,
                                            "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
                                    }
                             """"""


         ( verify user using following query from frontend to successfully login )
                            """"""
                                    mutation{
                                            verifyAccount(token:"eyJ1c2VybmFtZSI6ImhvbmV5IiwiYWN0aW9uIjoiYWN0aXZhdGlvbiJ9:1nJrWa:iU5pg3K7PoMwijik0ch_9R7-GT3MubgEStuSdHPr4d4")
                                            {
                                                    success
                                                    errors
                                            }
                                    }
                            """"""



6) Log a user in (LOGIN)
        extend your schema to login add the following LOC in your first mutation class "token_auth = mutations.ObtainJSONWebToken.Field()".

                            """"""
                                    class AuthMutation(graphene.ObjectType):
                                            register = mutations.Register.Field()           # regiter new user
                                            verify_account = mutations.VerifyAccount.Field()        # verify
                                            token_auth = mutations.ObtainJSONWebToken.Field()       # login
                            """"""

        extend your GRAPHQL_JWT by adding "graphql_auth.mutations.ObtainJSONWebToken" in settings.py
                            """"""
                                    GRAPHQL_JWT ={
                                        "JWT_ALLOW_ANY_CLASSES": [
                                            "graphql_auth.mutations.Register",
                                            "graphql_auth.mutations.VerifyAccount",
                                            "graphql_auth.mutations.ObtainJSONWebToken",
                                        ],
                                        "JWT_VERIFY_EXPIRATION": True,
                                        "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
                                    }
                            """"""


        (login user from frontend and access information about user from following query )

                            """"""
                                   mutation{
                                      tokenAuth(username:"<usernam>", password:"<passwrd>")
                                      {
                                        success
                                        errors
                                        token
                                        refreshToken
                                        user{
                                            username
                                          email
                                        }
                                      }
                                    }
                            """"""


7) Update Account

        extend your schema using "update_account = mutations.UpdateAccount.Field()"

        now if we run the following query for updateAccount it won't work however it work for super users,
        bcoz in order for normal user to update they need to authenticate themselves i.e. they need a JWT token to pass that across the server to identify the user as logged in

                           """"""
                                mutation{
                                    updateAccount(firstName:"<FNAME>")
                                    {
                                        success
                                        errors
                                    }
                                }
                           """"""

        for JWTokens we will use "Postman", it will allow us to stimulate the front end ;
         we will set up all of our queries here and send it across to our server

                    * install postman " sudo snap install postman " (this will help you run the postman software from your system)
                    * open postman software
                            1) create a new request
                            2) set request method to 'POST'
                            3) enter your request url i.e. "http://127.0.0.1:8000/graphql"
                            4) go to Headers section (below POST request) and set your KEY and VALUE
                                    i) set KEY to 'Authorization'
                                    ii) set VALUE to 'JWT <token_of_user>'
                            5) go to Body section (below POST request) and select GraphQL
                            6) add query in your QUERY section
                                    """"
                                        mutation{
                                            updateAccount(firstName:"<FNAME>")
                                            {
                                                success
                                                errors
                                            }
                                        }
                                    """"

                            7) press 'Send'

8) Resend Confirm email

        extend your schema using "resend_activation_email = mutations.ResendActivationEmail.Field()" and thats it


        now you can resend the verification mail again using following query:

                    """"""
                            mutation{
                                  resendActivationEmail(email:"<email>")
                                  {
                                    errors                  # here we will not utilize success bcoz we dont want any outsider to look or access at the emails available in the system
                                  }
                                }
                    """"""


9) Forgotten Password

        (users who will forget their password want ann email or link to change their password. )

        extend yor schema using "send_password_reset_email = mutations.SendPasswordResetEmail.Field()" and run the following query for the reset password mail

                    """"""
                            mutation{
                                  sendPasswordResetEmail(email:"<email>")
                                  {
                                    errors
                                    success
                                  }
                            }
                    """"""


        the above query will send a link into the terminal

                    example of link: "<p>http://127.0.0.1:8000/password-reset/eyJ1c2VybmFtZSI6ImdhcmltYSIsImFjdGlvbiI6InBhc3N3b3JkX3Jlc2V0In0:1nJv8z:jhTrf53qiYehbFb1pRPY5kjAawlEBLzhwiIjh7ii3IQ</p> ""


         now we need to actually allow them to reset the password; to achieve this extend your schema with "password_reset = mutations.PasswordReset.Field()" and run the query

                    """"""
                            mutation{
                                passwordReset(
                                    token:"<token from link",
                                    newPassword1:"pass1"
                                newPassword2:"pass2"
                                )
                                {
                                    errors
                                    success
                                }
                            }
                    """"""
