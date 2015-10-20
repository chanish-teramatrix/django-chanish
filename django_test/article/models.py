from django.db import models
from time import time
from django.db.models.signals import post_save

def get_upload_file_name(instance,filename):
	return "uploaded_files/%s_%s"  %(str(time()).replace('.','_'), filename)

# Create your models here.
class Article(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()
	pub_date = models.DateTimeField('date publish')
	likes = models.IntegerField(default=0)
	thumbnail = models.FileField(upload_to = get_upload_file_name, null=True)


	def __unicode__(self):
		return self.title


# class Comment(models.Model):
# 	name = models.CharField(max_length=200)
# 	body = models.TextField()
# 	pub_date = models.DateTimeField('date publish')
# 	article = models.ForeignKey(Article)

class UserInfo(models.Model):
	Gender = (
		('', 'Select'),
		('Male', 'male'),
		('Female', 'female')
	)
	first_name = models.CharField(max_length=10)
	last_name = models.CharField(max_length=15)
	email = models.EmailField()
	dob = models.DateTimeField()
	nick_name = models.CharField(max_length=8)
	gender = models.CharField(max_length=10, choices=Gender)
	password = models.CharField(max_length=8)
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.first_name


class Signal(models.Model):
	user = models.CharField(max_length = 10, blank=False)

	def __unicode__(self):
		return self.user


def signaltest_receiver(sender, instance=None, create=False, **kwargs):
	print "\n__________success____________________\n"

post_save.connect(signaltest_receiver, sender=Signal)

  
###signal handler

