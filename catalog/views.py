from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
# Create your views here.

def index(request):
    """
    Функция для отображения домашней страницы сайта.
    :param request: объект типа HttpRequest
    :return: сформированный Html шаблон
    """
    #Генерация количеств некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()
    #Генерация количества доступных книг (статус 'a')
    num_instance_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_custom_title = Book.objects.filter(title__icontains="Одиннадцать").count()

    #Отрисовка Html шаблона index.html с данными внутри
    return render(
        request,
        'index.html',
        context={'num_books':num_books, 'num_instance':num_instance, 'num_instance_available':num_instance_available, 'num_authors':num_authors, 'num_genres':num_genres, 'num_custom_title':num_custom_title},
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.ListView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.ListView):
    model = Author