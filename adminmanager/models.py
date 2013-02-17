from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey # зачем?!
from django.contrib import admin # админку принято конфигурировать в отдельном файле admin.py 

from PIL import Image # ну предположим, это когда-нибудь понадобится, хотя не понимаю зачем сложная библиотека по работе с картинками в хранилище паролей
import urllib # а это зачем?
import os # и это

class Users(models.Model): # 1) по большей части дублируется стандартная модель User, причём зря,
			   #    отсюда вытекает невозможность использовать стандартные батарейки: 
			   #    регистрацию, авторизацию, выход. Для них зачем-то написан велосипед, в добавок ко всему уязвимый, и это в системе хранения паролей! 
			   # 2) Модель принято называть в единственном числе, т.к. она описывает объект а не группу 
	login = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=30)
	email = models.EmailField(max_length=30)
	passwd = models.CharField(max_length=180)
	sex = models.BooleanField()
	wishes = models.TextField(max_length=256)

	def __unicode__(self):
		return self.login
# Правильно это делается вот так:
class Profile(models.Model):
	user = models.ForeignKey(User, related_name='profile')
	sex = models.BooleanField()
	wishes = models.TextField(max_length=256)

	def __unicode__(self):
		return self.user.username
# есть ещё вариант переопределить стандартную модель User
# но тогда придётся править админку, и другие стандартные батарейки для работы с новой моделью, 
# так что мне больше нравится первый вариант

class CSVBox(models.Model):
	title = models.CharField(max_length=30)
	login_base = models.CharField(max_length=30)
	password = models.CharField(max_length=32)
	url = models.CharField(max_length=120)
	users = models.ForeignKey(Users)
	bd_part = models.FileField(upload_to='hashing')
	
	def __unicode__(self):
		return self.title
