from django.db import models
from django.contrib.auth.models import AbstractUser            # we are using 'AbstractUser' coz we are going to extend from the existing model
# Create your models here.

class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")

    # to utilize both of the below fields we need to register them in the settings.py file using 'AUTH_USER_MODEL'

    USERNAME_FIELD = "username"     # utilising the username field
    EMAIL_FIELD = "email"           # utilising the email field





