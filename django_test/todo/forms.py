from django import forms
from models import User

class SignUp(form.ModelForm):
	class Meta:
		model = User
		fields = ['name','email','mobile','username','password']
		