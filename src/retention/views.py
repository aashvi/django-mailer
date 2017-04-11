from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives 
from django.http import HttpResponseRedirect
import os  
from email.mime.image import MIMEImage 
from retention.models import *
from django.utils import timezone
from .forms import CustomerForm
import csv


import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
# Create your views here. 


def email(request):
    
	template = get_template('index.html')
	context = Context({'user': 'AYUSH'})
	content = template.render(context)


	subject = "I am a text email"
	to = ['ayush@catchthatbus.com']
	from_email = 'CatchThatBus Team <noreply@catchthatbus.com>'

	msg = EmailMultiAlternatives(subject, content, from_email, to)  
	msg.content_subtype = 'html'  # Main content is text/html  
	msg.send()

    # EmailMessage(subject, message, to=to, from_email=from_email).send()

	return HttpResponse('email_one_through_view')



def imports(request):


	return HttpResponse('import_done')



def importclient(request):
	f = open('/users/ayush/Desktop/data.csv','rb')
	reader = csv.reader(f)

	for x in reader:
		q= Client(name= x[1], email = x[2], phone= x[3], email_sent=0, timestamp = timezone.now(), updated= timezone.now())
		q.save()

	return HttpResponse('import_done')



def temp(request):
	form = CustomerForm()
	return render(request, 'missyou.html')


def pdf(request):
    template = get_template('missyou.html')
    context = Context({'user': 'AYUSH'})
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


