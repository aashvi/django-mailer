from django import forms
from django.forms import ModelForm

from .models import Customer

class CustomerForm(forms.ModelForm):
	class Meta:
		model= Customer
		fields = ['name', 'phone', 'email', 'email_sent']
