# Create your views here.
from django.shortcuts import render , HttpResponse ,redirect 
from datetime import datetime
from test_app.models import Book,Author
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response

class get_all_books(APIView):
    #return HttpResponse("search page")
    def get(self, request):
        titles = [b.title1 for b in Book.objects.all()]
        return Response(titles)
    
    # Using pyhton coding 
    def total_copies_sold_for_author(self):
        # use this
        # author = Author.objects.annotate_with_copies_sold().first()
        # ax = Author.objects.annotate_with_copies_sold()
        # ax[1].copies_sold # 43 
        #or
        authors = Author.objects.all()
        for a in authors:
            b = Book.objects.filter(author = a).values('copies_sold')
            s = sum([x['copies_sold'] for x in b])
            print(a, b, 'total copies = ',s)
            '''
            runit <QuerySet [{'copies_sold': 12}, {'copies_sold': 2}, {'copies_sold': 5}]> 19
            tinu <QuerySet [{'copies_sold': 43}]> 43
            '''
