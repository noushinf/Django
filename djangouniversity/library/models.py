from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings


class Author(models.Model):
    name = models.CharField(max_length=200)
    birth = models.DateTimeField()
    death = models.DateTimeField(null=True, blank=True)

    # books = models.ManyToManyField('Books', through='Authored')

    def __str__(self):
        return self.name


class Authored(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language


class Place(models.Model):
    section = models.CharField(max_length=100)
    shelf = models.CharField(max_length=50)

    def __str__(self):
        return self.section


class Book(models.Model):
    name = models.CharField(max_length=200,
                            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")])
    publish_day = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    # author = models.ManyToManyField('Author', through='Authored')
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    description = models.TextField()
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    place = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    picture = models.BinaryField(null=True, editable=True)
    # picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='book_owner')

    def __str__(self):
        return self.name
