from django.db import models
from django.conf import settings


class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    company_name = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()


class Event(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    event_status = models.BooleanField()
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.CharField(max_length=400)
