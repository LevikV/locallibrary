from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
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

    #Показ количества посещений пользователем главной страницы
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits +1


    #Отрисовка Html шаблона index.html с данными внутри
    return render(
        request,
        'index.html',
        context={'num_books':num_books, 'num_instance':num_instance, 'num_instance_available':num_instance_available, 'num_authors':num_authors, 'num_genres':num_genres, 'num_custom_title':num_custom_title, 'num_visits':num_visits},
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Представление отображения списка книг, взятых на прокат для текущего пользователя
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
#Переопределяем вывод отфильтровав значения
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksList(PermissionRequiredMixin, generic.ListView):
    """
    Представление для администрации для отображения всех выданных книг
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'
#Переопределяем вывод отфильтровав значения
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')