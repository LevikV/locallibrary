from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)

#Регистрация нового класса для изменения отображения админки для Author

class BookInline(admin.TabularInline):
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_die')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_die')]
    BookInline.extra = 0
    inlines = [BookInline]


admin.site.register(Author, AuthorAdmin)

#Регистрация нового класса для изменения отображения админки для Book

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    BookInstanceInline.extra = 0
    inlines = [BookInstanceInline]

#Регистрация нового класса для изменения отображения админки для BookInstance

@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None,{'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back')})
    )