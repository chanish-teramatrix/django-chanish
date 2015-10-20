from django.db import models
from time import time


class User(models.Model):
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=20)
	mobile = models.IntegerField(primary_key=True)	
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=10)

	def __unicode__(self):
		return self.username
		