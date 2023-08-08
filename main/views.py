from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from .models import *
from .services import mongoDriver
from .tasks import *
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


# def update_names(request):
#     if 'pswd' in (x := request.GET):
#         if x['pswd'] == '123qwe':
#             update_names_task.delay()
#             return HttpResponse(status=200)
#     return HttpResponse(status=405)
#
#
def update(request):
    update_items_task.delay()
    return HttpResponse(status=200)
#
#
# @api_view(['GET'])
# def get_item(request):
#     data_response = mongoDriver.get(dict(request.GET))
#     status = 404
#     if data_response:
#         status = 200
#     response = JsonResponse(data_response, status=status)
#     response['Access-Control-Allow-Origin'] = '*'
#     response['timezone'] = 'UTC+0'
#     return response
#
#
# @api_view(['POST'])
# def signup(request):
#     print(request.session)
#     # username = request.POST['user']
#     # password = request.POST['pass']
#     return HttpResponse(status=200)
#
#
# @api_view(['POST'])
# def login(request):
#     print(request.GET)
#     username = request.GET['user']
#     password = request.GET['pass']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         token = Token.objects.create(user=user)
#         print(token.key)
#     else:
#         pass
#
#     return HttpResponse(status=200)

# No backend authenticated the credentials
