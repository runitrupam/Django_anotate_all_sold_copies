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
        self.total_copies_sold_for_author() # TO SHOW YOU WHAT IS ANNOTATE
        return Response(titles)
    def post(self,request):
        print(request)
        '''
        {
        "title1" : "learning Django",
        "copies_sold" : 45,
        "author" : "runit"
        }
        '''
        title1 = request.data['title1']
        copies_sold = request.data['copies_sold']
        ob = Book(title1 = title1 ,copies_sold = copies_sold )
        ob.save()
        # author
        titles = [b.title1 for b in Book.objects.all()]
        return Response(titles)
    def put(self,request):
        print(request,'update')
        titles = [b.title1 for b in Book.objects.all()]
        return Response(titles)
    # Using pyhton coding 
    def total_copies_sold_for_author(self):
        # use this
        author = Author.objects.annotate_with_copies_sold().first()
        ax = Author.objects.annotate_with_copies_sold()
        for i in range(len(ax)):
            print( ax[i] , ax[i].copies_sold  )

        '''
        Note , annotate_with_copies_sold =
        query = SELECT "author"."id", "author"."first_name", "author"."last_name",
                COALESCE(SUM("book"."copies_sold"), 0) AS "copies_sold"
                FROM "author" LEFT OUTER JOIN "book"
                        ON ("author"."id" = "book"."author_id")
                GROUP BY "author"."id", "author"."first_name", "author"."last_name" ;
        BEST THING IS , INSTEAD OF USING ANNOTATE USE , CUSTOM QUERY .
        SEE BELOW
        '''

        authors = Author.objects.all()
        for a in authors:
            b = Book.objects.filter(author = a).values('copies_sold')
            s = sum([x['copies_sold'] for x in b])
            print(a, b, 'total copies = ',s)
            '''
            runit <QuerySet [{'copies_sold': 12}, {'copies_sold': 2}, {'copies_sold': 5}]> 19
            tinu <QuerySet [{'copies_sold': 43}]> 43
            '''
