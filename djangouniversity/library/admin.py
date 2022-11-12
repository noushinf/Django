from django.contrib import admin
from library.models import Book, Category, Language, Author, Place


class PicAdmin(admin.ModelAdmin):
    exclude = ('picture', 'content_type')


admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Place)

