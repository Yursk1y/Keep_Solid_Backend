from datetime import datetime, timedelta
from django.http import HttpResponse

import jwt
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from Api.settings import SECRET_KEY
from .models import User
from .forms import UserModel
from django.db.utils import IntegrityError

def responce_return(massage, cookie, user_name):
    response = HttpResponse(massage)
    response.set_cookie(key='token', value=cookie, httponly=True, expires=datetime.today() + timedelta(days=365))
    response.set_cookie(key='user_name', value=user_name, httponly=True, expires=datetime.today() + timedelta(days=365))
    return response

def get_cookie(request):
    try:
        cookie = request.COOKIES.get('token')
        user_name = request.COOKIES.get('user_name')
        token_data = jwt.decode(cookie, SECRET_KEY, algorithms=['HS256'])
        creation_date = datetime.strptime(token_data["creation_date"], "%x")
        user = User.objects.filter(email=token_data['login']).first()
        if creation_date < datetime.today() - timedelta(days=7):
            raise jwt.exceptions.InvalidTokenError
        if not user.password == token_data['password']:
            raise jwt.exceptions.InvalidTokenError
        if creation_date <= datetime.today() - timedelta(days=1):
            cookie = user.token
        return user, cookie, user_name
    except jwt.exceptions.InvalidTokenError:
        return False, cookie, False

@csrf_exempt
def Auth(request):
    try:
        user, cookie, user_name = get_cookie(request)
        if not user:
            user_data = JSONParser().parse(request)
            if request.method == 'LOGIN':
                user = User.objects.filter(email=user_data["email"]).first()
                if user is None:
                    return HttpResponse("Login or pass is incorrect")
                if not user.check_password(user_data["password"]):
                    print(user.password)
                    return HttpResponse("Login or pass is incorrect")
                return responce_return("Successfully logged in", user.token, user.email)
            
            elif request.method == 'REGISTER':
                new_user = UserModel(data=user_data)
                if new_user.is_valid():
                    new_user.create(new_user.cleaned_data)
                    user = User.objects.filter(email=user_data["email"]).first()
                    return responce_return("Successfully registered", user.token, user.email)
                else:
                    return HttpResponse("Wrong data.")
            else:
                return HttpResponse("Method is not allowed for you.")
                
        elif user:
            if request.method == 'LOGOUT':
                response = HttpResponse("Succesfully logged out")
                response.delete_cookie("token")
                response.delete_cookie("user_name")
                return response
            


            elif request.method == 'USER_EDIT':
                try:
                    new_data = JSONParser().parse(request)
                    edit_user = user
                    new_data.pop("list_of_favorite_books")
                    new_data.pop("role")
                    if "password" in new_data.keys():
                        edit_user.set_password(new_data["password"])
                        new_data.pop("password")
                    edit_user.__dict__.update(new_data)
                    edit_user.save()
                    return responce_return("Successfully edited", user.token, user.email)
                except Exception as error:
                    return HttpResponse(error)
            else:
                return HttpResponse("Method is not allowed for you.")
        else:
            return HttpResponse("Method is not allowed for you.")
    except KeyError:
        return JsonResponse("Some data is wrong.", safe=False) 
    except (jwt.exceptions.DecodeError, ):
        return JsonResponse("Invalid token.", safe=False)
    except IntegrityError:
        return JsonResponse("This email already exists.", safe=False)
    except Exception as err:
        print(err)
        return JsonResponse(f"An error occurred: {err}", safe=False)
