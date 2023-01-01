from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce

class AuthorManager(models.Manager):
    def get_queryset(self):
        return AuthorQuerySet(self.model, using=self._db)

    def annotate_with_copies_sold(self):
        return self.get_queryset().annotate_with_copies_sold()


class AuthorQuerySet(models.QuerySet):
    def annotate_with_copies_sold(self):
        return self.annotate(copies_sold=Coalesce(Sum('books__copies_sold'), 0))

# class AuthorManager(models.Manager):
    #def total_copies_sold(self):
    #     return self.get_queryset().annotate(copies_sold=Sum('books__copies_sold'))

# class AuthorQuerySet(models.QuerySet):
#     def annotate_with_copies_sold(self):
#         return self.annotate(copies_sold = Sum('books__copies_sold'))

class Author(models.Model):
    objects = AuthorManager()
    first_name = models.CharField(max_length=121)
    last_name = models.CharField(max_length=120)
    def __str__(self):
        return self.first_name
    class Meta:
        db_table = 'author'
class Book(models.Model):
    title1 = models.CharField(max_length=100)
    copies_sold = models.PositiveIntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    def __str__(self):
        return self.title1
    class Meta:
        db_table = 'book'