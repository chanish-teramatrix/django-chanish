from django import forms
from models import Article, UserInfo, Signal
import logging
from datetime import datetime


class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['title', 'body', 'pub_date', 'thumbnail']


class ProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		self.base_fields['first_name'].label = 'First Name'
		self.base_fields['last_name'].label = 'Last Name'
		self.base_fields['nick_name'].label = 'Nick Name'
		self.base_fields['dob'].label = 'Date Of Birth'

		super(ProfileForm, self).__init__(*args, **kwargs)


	class Meta:
		model = UserInfo
		fields = ['first_name', 'last_name', 'email', 'dob', 'nick_name', 'gender',
				  'password']


class SignalForm(forms.ModelForm):
	class Meta:
		model = Signal
		fields = ['user']


class EmailForm(forms.Form):
	subject = forms.CharField(max_length=100, label='Subject', required=True)
	message = forms.CharField(max_length=300, label='Message', required=True)
	from_email = forms.EmailField(label='From', required=True)
	to_email = forms.EmailField(label='To', required=True)

	def clean(self):
		from_email = self.cleaned_data.get('from_email')
		to_email = self.cleaned_data.get('to_email')
		try:
			if from_email == to_email:
				print('sender and receiver are same')
				self.errors['from_email'] = ErrorList(u'sender and receiver are same')
				self.errors['to_email'] = ErrorList(u'sender and receiver are same')
		except Exception as e:
			logging.getLogger(e.message)

		return self.cleaned_data
