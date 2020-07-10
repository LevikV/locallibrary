from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    #url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my_borrowes'),
]