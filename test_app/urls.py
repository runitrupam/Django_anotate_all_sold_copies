
from django.contrib import admin
from django.urls import path
from .views import get_all_books


urlpatterns = [
    path('books/',  get_all_books.as_view() ) , # list of books home page
]

