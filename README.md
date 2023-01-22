# Django_anotate_all_sold_copies

TO UNDERSTAND THE WORKING OF annotate

FIRST GO TO MODELS.PY AND THEN TO VIEW.PY
author is a foreign key of book .
So I want to know all the total copies of book sold for a particular author .
Anno


In this I have used RestAPI Framework 
`GET , PUT, POST is used . `
 
Note , annotate_with_copies_sold 
```
query = SELECT "author"."id", "author"."first_name", "author"."last_name",
        COALESCE(SUM("book"."copies_sold"), 0) AS "copies_sold"
        FROM "author" LEFT OUTER JOIN "book"
                ON ("author"."id" = "book"."author_id")
        GROUP BY "author"."id", "author"."first_name", "author"."last_name" ;
 ```
BEST THING IS , INSTEAD OF USING ANNOTATE USE , CUSTOM QUERY .
 ```
authors = Author.objects.all()
for a in authors:
    b = Book.objects.filter(author = a).values('copies_sold')
    s = sum([x['copies_sold'] for x in b])
    print(a, b, 'total copies = ',s)
 ```
Or USE  ```res = pd.read_sql(query) ```
