from django.contrib import admin
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives 

import os  
from email.mime.image import MIMEImage 

# Register your models here.
from .models import *
import httplib
import ssl





admin.site.register(Customer, CustomerAdmin)

admin.site.register(MarketingCampaign,MarketingCampaignAdmin )
admin.site.register(Client, ClientAdmin)