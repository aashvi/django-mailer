from __future__ import unicode_literals
import httplib
import ssl
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from django.forms import ModelForm
from django import forms
from time import sleep

from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives 
import os  
from email.mime.image import MIMEImage 
import re,csv, json



# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=120, null=True, blank= True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    email_sent = models.IntegerField()
    timestamp =models.DateTimeField(auto_now_add=True, auto_now=False)
    updated =models.DateTimeField(auto_now_add=False, auto_now=True)


    """docstring for Signup"""

    def __str__(self):
        return self.name



class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','phone','email_sent')
    
    actions = ['send_email','test_send']

    def send_email(self, request, queryset):
        l= []
        for obj in queryset:
            if obj.email_sent<1:
                # template = get_template('test.html')
                template = get_template('missyou.html')

                context = Context({'user': str(obj.name).title()})
                content = template.render(context)
                subject = "Hey "+str(obj.name).title()+", We are missing you !"
                to = [obj.email]
                from_email = 'CatchThatBus Team <noreply@catchthatbus.com>'


                msg = EmailMessage(subject, content, from_email, to)  
                msg.content_subtype = 'html'  # Main content is text/html  
                msg.send()

                conn = httplib.HTTPConnection("api.infobip.com")

                c=[]
                c.append('"'+str(obj.phone)+'"')
                c= re.sub(r'[^\w]', '', c[0])


                payload = "{\"from\":\"CTB\",\"to\":" + c + ",\"text\":\" CatchThatBus: Hi, We are missing you! Use code MISSYOU for 10"+"%"+" off your bus tickets purchase. Book today https://goo.gl/pS0Qui.\"}"

                headers = {
                        'authorization': "",
                        'content-type': "application/json",
                        'accept': "application/json"
                        }


                conn.request("POST", "/sms/1/text/single", payload, headers)
               
                
                
        queryset.update(email_sent=1)
        






    def test_send(self, request, queryset):
        l= []
        for obj in queryset:
            if obj.email_sent<1:
                # template = get_template('test.html')
                template = get_template('missyou.html')

                context = Context({'user': str(obj.name).title()})
                content = template.render(context)
                subject = "Hey "+str(obj.name).title()+", We are missing you !"
                to = [obj.email]
                from_email = 'CatchThatBus Team <noreply@catchthatbus.com>'
                # headers = 


                msg = EmailMessage(subject, content, from_email, to, headers= {'Reply-To': 'ayush@catchthatbus.com','X-SMTPAPI': {"category":"MISS"}})  
                msg.content_subtype = 'html'  # Main content is text/html  
                msg.send()


                
                
        # queryset.update(email_sent=1)
    send_email.short_description = "send email & sms"
    test_send .short_description = "Send a test mail"








        
class Client(models.Model):
    name = models.CharField(max_length=120, null=True, blank= True)
    email = models.EmailField()
    phone = models.CharField(max_length=20,null=True, blank=True)
    email_sent = models.IntegerField()
    timestamp =models.DateTimeField(auto_now_add=True, auto_now=False)
    updated =models.DateTimeField(auto_now_add=False, auto_now=True)
    def __str__(self):
        return self.name

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','phone','email_sent')
    
    actions = ['send_email']


class MarketingCampaign(models.Model):
    name = models.CharField(max_length=50)
    client = models.ManyToManyField(Client, null= True, blank=True)
    description = models.CharField(max_length=300)
    import_done = models.BooleanField()
    activated= models.BooleanField(default= False)
    subject_line =models.CharField(max_length=300, null=True, blank=True)
    template= models.FileField(max_length=100 , null= True, blank=True)
    customer_data = models.FileField(max_length=100 , null= True, blank=True)
    smstext =models.CharField(max_length=300, default='')

    def __str__(self):
        return self.name




class MarketingCampaignAdmin(admin.ModelAdmin):


    list_display = ('id','name','description','import_done','activated','subject_line','template','customer_data','smstext')
    
    ## Importing data from local
    actions = ['import_data','send_email_sms']
    def import_data(self, request, queryset): 
        for obj in queryset:
            if obj.import_done==False:
                reader = csv.reader(obj.customer_data)

                for x in reader:
                    q= Client(name= x[1], email = x[2], phone= x[3], email_sent=0, timestamp = timezone.now(), updated= timezone.now())
                    q.save()
                    obj.client.add(q)

        queryset.update(import_done=True)
        return HttpResponse('import_done') 
    import_data.short_description = "import data from local "




    ### Activating the 
    def send_email_sms(self, request, queryset):
        
        for obj in queryset:
            if (obj.import_done==True and obj.activated==False):
                for clnt in obj.client.all():
                    if clnt.email_sent<1:

                        template = get_template('missyou.html')

                        context = Context({'user': str(clnt.name).title()})
                        content = template.render(context)
                        subject = "Hey "+str(clnt.name).title()+", We are missing you !"
                        to = [clnt.email]
                        from_email = 'CatchThatBus Team <noreply@catchthatbus.com>'


                        msg = EmailMessage(subject, content, from_email, to)  
                        msg.content_subtype = 'html'  # Main content is text/html  
                        msg.send()

                        conn = httplib.HTTPConnection("api.infobip.com")

                        c=[]
                        c.append('"'+str(clnt.phone)+'"')
                        c= re.sub(r'[^\w]', '', c[0])


                        payload = "{\"from\":\"CTB\",\"to\":" + c + ",\"text\":\" CatchThatBus: Hi, We are missing you! Use code MISSYOU for 10"+"%"+" off your bus tickets purchase. Book today https://goo.gl/pS0Qui.\"}"

                        headers = {
                                'authorization': "",
                                'content-type': "application/json",
                                'accept': "application/json"
                                }


                        conn.request("POST", "/sms/1/text/single", payload, headers)

                        queryset.update(activated=True)     
            
    send_email_sms.short_description = "send_result"




