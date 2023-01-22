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
        books = [(b.id,b.title1,"Author :"  + b.author.first_name) for b in Book.objects.all()]
        self.total_copies_sold_for_author() # TO SHOW YOU WHAT IS ANNOTATE
        return Response(books)

    def post(self,request):
        print(request,'add new books , so idempotent as ur db is changed everytime , on same api call')
        '''
        {
        "title1" : "learning Django",
        "copies_sold" : 45,
        "author" : "runit"
        }
        '''
        title1 = request.data['title1']
        copies_sold = request.data['copies_sold']
        author_first_name = request.data['author']
        author = Author.objects.filter(first_name=author_first_name).first()
        # here we have to pass a instance of class Author to the field author . i.e y I am using .first() instead of values
        ob = Book(title1 = title1 ,copies_sold = copies_sold , author = author )
        ob.save()
        # author
        titles = [b.title1 for b in Book.objects.all()]
        return Response(titles)

    def put(self,request):
        print(request,'update a part of book , not idempotent as ur db is changed only once, on same api call')
        # NOTE : Change only those parts of book , which can be changed .
        '''
        {
        "book_id": 6,
        "title1" : "learning Django2",
        "copies_sold" : 45,
        "author" : "runit"
        }
        
        '''
        book = request.data
        book_id = book['book_id']
        title1 = book.get('title1', None)
        copies_sold = book.get('copies_sold', None)
        author_first_name = book.get('author', None)
        if author_first_name :
            author = Author.objects.filter(first_name=author_first_name).first()
        else:
            author = None


        try :
            book_ob = Book.objects.get(id=book_id)
            book_ob.title1 = title1 if title1 else book_ob.title
            book_ob.copies_sold = copies_sold if copies_sold else book_ob.copies_sold
            book_ob.author = author if author else book_ob.author
            book_ob.save()
        except Exception as e :
            print('issue in getting object of book during a PUT API request' ,e )
        b = book_ob
        return Response((b.id,b.title1,b.author.first_name,b.copies_sold))


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
