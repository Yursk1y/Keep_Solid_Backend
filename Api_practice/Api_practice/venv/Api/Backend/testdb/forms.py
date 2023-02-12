from rest_framework import serializers
from django import forms

from .models import User, Book, Author, Genre
from django.contrib.auth.hashers import make_password


class UserModel(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'role', 'list_of_favorite_books')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    """ #data example
    {
    "email":"mysql@gmail.com",
    "password":"one",
    "role":"user",
    "list_of_favorite_books":"1,2"
    }
    """
    
    
class BookModel(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('name', 'id_author', 'id_genre', 'date_of_issue')

    """ #data example
    {
    "name":"FirstBook",
    "id_author":"2",
    "id_genre":"1",
    "date_of_issue":"1995.07.12"
    }
    """

class AuthorModel(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name',)

class GenreModel(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('name',)
