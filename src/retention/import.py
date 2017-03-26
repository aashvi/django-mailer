from retention.models import *
from django.utils import timezone


import csv

f = open('/users/ayush/Desktop/data.csv','rb')
reader = csv.reader(f)

for x in reader:
	q= Customer(name= x[1], email = x[2], phone= x[3], email_sent=0, timestamp = timezone.now(), updated= timezone.now())
	q.save()
