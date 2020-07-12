from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from .form import RenewBookForm
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
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

#Функция для работы с формами
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('booksloans') )

    # Если это GET (или какой-либо еще), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_die':'12/10/2016',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_die']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

