from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from .forms import *
from .models import  Book
from array import *
from datetime import date
from .auth import get_cookie, responce_return

import csv
from django.http import FileResponse



# Create your views here.
@csrf_exempt
def Librare(request):
        parsed_data = JSONParser().parse(request)

        if request.method == 'BOOKS_LIST':                  #done
            response = ""
            data = Book.objects.values()
            if data.__len__() == 0:
                return HttpResponse("Empty table.")
            else:
                for record in data:
                    response+=str({"Название":record["name"]})+"\n"
                return HttpResponse(response)
        if request.method == 'BOOKS_INFO':                #done
            book = Book.objects.get(name=parsed_data["name"])
            if book:
                book_data = {}
                book_data["Название"]=book.name
                book_data["Автор"] = ", ".join([Author.objects.get(id=int(i)).get_username() for i in book.id_author])
                book_data["Жанр"] = ", ".join([Genre.objects.get(id=int(i)).get_username() for i in book.id_genre])
                book_data["Дата написания"] = str(book.date_of_issue)
                return HttpResponse(str(book_data))
            else:
                return HttpResponse("Not valid data or this user already exists.")  
         
            
        user, cookie, user_name = get_cookie(request)

        if user:
            if request.method == 'BOOKS_NEW' and user.role == "admin": #done
                date_book = [int(i) for i in parsed_data['date_of_issue'].split('.')] 
                parsed_data['date_of_issue'] = date(date_book[0],date_book[1],date_book[2])
                parsed_data["id_genre"] = [str(i) for i in parsed_data["id_genre"].split(",")]
                parsed_data["id_author"] = [str(i) for i in parsed_data["id_author"].split(",")]
                book_record = BookModel(data=parsed_data)
                if book_record.is_valid():
                    book_record.save()
                    return responce_return("Record created.", cookie,user_name)
                else:
                    return responce_return("Not valid data or this book already exists.", cookie,user_name)
                  
            elif request.method == 'BOOKS_DELETE_ADMIN' and user.role == "admin": #done
                response = []
                book_record = Book.objects.get(name=parsed_data["name"])
                if book_record:
                    book_record.delete()
                    return responce_return("Record deleted.", cookie, user_name)
                else:
                    return responce_return("No such record", cookie, user_name)
                
            elif request.method == 'FAVLIST_EDIT':
                user.list_of_favorite_books = [str(i) for i in parsed_data["list_of_favorite_books"].split(",")]
                user.save()
                return HttpResponse("Succesfully edited!")
            
            elif request.method == 'CSV_LIB':
                try:
                    data = Book.objects.values()
                    if not data.__len__() == 0:
                        
                        with open('Api/Backend/Template/table.csv', 'w', newline='', encoding='UTF-8') as csvfile:
                            writer = csv.writer(csvfile, delimiter=' '
                                                    , quoting=csv.QUOTE_MINIMAL)
                            fieldnames = ['Название','Автор',"Жанр","Дата написания"]
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,quotechar=';') 
                            writer.writeheader()
                            for record in data:
                                book_data = {}
                                book_data["Название"]=record["name"]
                                book_data["Автор"] = " ".join([Author.objects.get(id=int(i)).get_username() for i in record["id_author"]])
                                book_data["Жанр"] = " ".join([Genre.objects.get(id=int(i)).get_username() for i in record["id_genre"]])
                                book_data["Дата написания"] = str(record["date_of_issue"])
                                writer.writerow(book_data)
                            return FileResponse(open('Api/Backend/Template/table.csv','rb'))
                    else: 
                        return HttpResponse("Empty table.")
                except Exception as error:
                    return HttpResponse(error)
                finally:
                    if csvfile:
                        csvfile.close()
            else:
                return responce_return("This methon is not allowed for you.", cookie, user_name) 
            
        else:
            return HttpResponse("You have to log in first.") 
            

            