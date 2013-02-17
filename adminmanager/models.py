from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.contrib import admin

from PIL import Image
import urllib
import os

class Users(models.Model):
	login = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=30)
	email = models.EmailField(max_length=30)
	passwd = models.CharField(max_length=180)
	sex = models.BooleanField()
	wishes = models.TextField(max_length=256)

	def __unicode__(self):
		return self.login

class CSVBox(models.Model):
	title = models.CharField(max_length=30)
	login_base = models.CharField(max_length=30)
	password = models.CharField(max_length=32)
	url = models.CharField(max_length=120)
	users = models.ForeignKey(Users)
	bd_part = models.FileField(upload_to='hashing')
	
	def __unicode__(self):
		return self.title