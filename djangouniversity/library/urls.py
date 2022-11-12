from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [

    path('', views.MainView.as_view(), name='all'),
    # path('book/<int:pk>', views.BookCreateView.as_view(), name='ad_detail'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/create', views.BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/update',
         views.BookUpdateView.as_view(), name='book_update'),
    path('book/<int:pk>/delete',
         views.BookDeleteView.as_view(), name='book_delete'),
    path('book_picture/<int:pk>', views.stream_file, name='book_picture'),
    path('language/', views.LanguageView.as_view(), name='language_list'),
    path('language/create/', views.LanguageCreateView.as_view(), name='language_create'),
    path('language/<int:pk>/update', views.LanguageUpdateView.as_view(), name='language_Update'),
    path('language/<int:pk>/delete', views.LanguageDeleteView.as_view(), name='language_Delete'),
    path('place/', views.PlaceView.as_view(), name='place_list'),
    path('place/create/', views.PlaceCreateView.as_view(), name='place_create'),
    path('place/<int:pk>/update', views.PlaceUpdateView.as_view(), name='place_Update'),
    path('place/<int:pk>/delete', views.PlaceDeleteView.as_view(), name='place_Delete'),
    path('category/', views.CategoryView.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view(), name='category_Update'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category_Delete'),
    path('author/', views.AuthorView.as_view(), name='author_list'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name='author_Update'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='author_Delete'),

]
