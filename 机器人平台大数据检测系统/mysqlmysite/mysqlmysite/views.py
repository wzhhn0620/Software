from django.shortcuts import render,redirect
from django.http import HttpResponse
import pymysql
from utils import sqlheper


def machine_login(request):
    return redirect('./userlogin/')