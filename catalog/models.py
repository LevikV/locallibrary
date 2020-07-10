from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Genre(models.Model):
    """
    Модель представления жанра книги (Научная фантастика, Фантастика, Художественная и т.д.)
    """

    name = models.CharField(max_length=200, help_text="Введите жанр книги")

    def __str__(self):
        """
        Строка возвращаемая объектом модели (в т.ч. в Админке)
        """
        return self.name

class Language(models.Model):
    """
    Модель определения языка для книг
    """
    name = models.CharField(max_length=200, help_text="Введите язык книги")

    def __str__(self):
        return self.name

from django.urls import reverse

class Book(models.Model):
    """
    Модель представления книги
    """

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Введите описание книги")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN номера</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр книги")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        Строка возвращаемая данным объектом
        """
        return self.title

    def get_absolute_url(self):
        """
        Возвращает URL для доступа к конкретному экземпляру книги
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Cоздает строку Жанров для отображения в админке"""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'

import uuid

class BookInstance(models.Model):
    """
    Модель представляющая запись о книге (которую взяли из библиотеки)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для этого экземпляра книги")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'На обслуживании'),
        ('o', 'Выдана'),
        ('a', 'Доступна'),
        ('r', 'Зарезервирована'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text="Доступность книги")

#Функция проверки просрочки даты возврата книги
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        Строка возвращаемая данным объектом
        """
        return ' %s (%s)' % (self.id, self.book.title)

class Author(models.Model):
    """
    Модель представления автора книги
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_die = models.DateField('Died', null=True, blank=True)

    def __str__(self):
        return '{1}, {0}' .format(self.last_name, self.first_name)

    class Meta:
        ordering = ['first_name']

    def get_absolute_url(self):
        """
        Возвращает URL для доступа к конкретному экземпляру книги
        """
        return reverse('author-detail', args=[str(self.id)])