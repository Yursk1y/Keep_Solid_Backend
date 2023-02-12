from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
import jwt
import secrets
from Api.settings import SECRET_KEY
from datetime import *

class User(AbstractBaseUser):
    class Role(models.TextChoices):
        user = "user",
        admin = "admin"
    email = models.EmailField(max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    role = models.CharField(max_length=5, choices=Role.choices, default=Role.user)
    list_of_favorite_books = ArrayField(base_field=models.CharField(max_length=6, blank=True) )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        token = jwt.encode({
            'salt': secrets.token_urlsafe(32),
            'creation_date': datetime.today().strftime("%x"),
            'login': self.email,
            'password': self.password
        }, SECRET_KEY, algorithm='HS256')
        return token

    

class Book(AbstractBaseUser):
    name = models.CharField(max_length=50, unique=True)
    id_author = ArrayField(base_field=models.CharField(max_length=6) )
    id_genre = ArrayField(base_field=models.CharField(max_length=6) )
    date_of_issue = models.DateField()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []


class Author(AbstractBaseUser):
    name = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

class Genre(AbstractBaseUser):
    name = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []
