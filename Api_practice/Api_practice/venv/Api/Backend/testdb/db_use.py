from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from .forms import *
from .models import User, Book
from array import *
from datetime import date
from .auth import get_cookie


# Create your views here.
@csrf_exempt
def Parser(request):
    parsed_data = JSONParser().parse(request)
    user, cookie, user_name = get_cookie(request)
    if user:

        if user.role == "admin":

            if request.method == 'USERS_GET':
                response = User.objects.values()
                if response.__len__() == 0:
                    return HttpResponse("Empty table.")
                else:
                    for record in response:
                        record.pop("id")
                        record.pop("last_login")
                    return HttpResponse(response)

            elif request.method == 'USERS_CREATE':
                parsed_data["list_of_favorite_books"] = [
                    str(i) for i in parsed_data["list_of_favorite_books"].split(",")]
                response = []
                user_record = UserModel(data=parsed_data)
                if user_record.is_valid():
                    user_record.create(user_record.cleaned_data)
                    return HttpResponse("Record created.")
                else:
                    return HttpResponse("Not valid data or this user already exists.")

            elif request.method == 'USERS_DELETE':
                response = []
                user_record = User.objects.get(email=parsed_data["email"])
                if user_record:
                    user_record.delete()
                    return HttpResponse("Record deleted.")
                else:
                    return HttpResponse("No such record.")

            elif request.method == 'BOOKS_GET':
                response = Book.objects.values()
                if response.__len__() == 0:
                    return HttpResponse("Empty table.")
                else:
                    for record in response:
                        record.pop("id")
                        record.pop("last_login")
                        record.pop("password")
                    return HttpResponse(response)

            elif request.method == 'BOOKS_CREATE':
                response = []
                date_book = [int(i)
                             for i in parsed_data['date_of_issue'].split('.')]
                date_book.reverse()
                parsed_data['date_of_issue'] = date(
                    date_book[0], date_book[1], date_book[2])
                book_record = BookModel(data=parsed_data)
                if book_record.is_valid():
                    book_record.save()
                    return HttpResponse("Record created.")
                else:
                    return HttpResponse("Not valid data or this book already exists.")
                
            elif request.method == 'BOOKS_DELETE':
                response = []
                book_record = Book.objects.get(name=parsed_data["name"])
                if book_record:
                    book_record.delete()
                    return HttpResponse("Record deleted.")
                else:
                    return HttpResponse("No such record.")

            elif request.method == "GENRES_GET":
                response = ""
                data = Genre.objects.values()
                for record in data:
                    record.pop("password")
                    record.pop("last_login")
                    response += str(record)+"\n"
                return HttpResponse(response)

            elif request.method == "GENRES_CREATE":
                genre_record = GenreModel(data=parsed_data)
                if genre_record.is_valid():
                    genre_record.save()
                    return HttpResponse("Record complete.")
                else:
                    return HttpResponse("No valid data.")

            elif request.method == "GENRES_DELETE":
                genre_record = Genre.objects.get(name=parsed_data["name"])
                if genre_record:
                    genre_record.delete()
                    return HttpResponse("Record deleted.")
                else:
                    return HttpResponse("No such record.")

            elif request.method == "AUTORS_GET":
                response = ""
                data = Author.objects.values()
                for record in data:
                    record.pop("password")
                    record.pop("last_login")
                    response += str(record)+"\n"
                return HttpResponse(response)

            elif request.method == "AUTORS_CREATE":
                author_record = AuthorModel(data=parsed_data)
                if author_record.is_valid():
                    author_record.save()
                    print(author_record)
                    return HttpResponse("Record complete.")
                else:
                    return HttpResponse("No valid data.")

            elif request.method == "AUTORS_DELETE":
                response = []
                author_record = Author.objects.get(name=parsed_data["name"])
                if author_record:
                    author_record.delete()
                    return HttpResponse("Record deleted.")
                else:
                    return HttpResponse("No such record.")
            else:
                print("A?")
                return HttpResponse("This method does not exists.")
        else:
            return HttpResponse("You have not enought rights.")
    else:
        return HttpResponse("Invalid token.")
