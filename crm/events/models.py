from django.db import models
from django.conf import settings


class Client(models.Model):
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    email = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    mobile = models.CharField(max_length=20, blank=False)
    company_name = models.CharField(max_length=250, blank=False)
    date_created = models.DateField(auto_now_add=True, blank=False)
    date_updated = models.DateField(auto_now_add=True, blank=False)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False
    )


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False
    )
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        related_name='contracts',
        blank=False,
    )
    date_created = models.DateField(auto_now_add=True, blank=False)
    date_updated = models.DateField(auto_now_add=True, blank=False)
    signed_status = models.BooleanField(default=False)
    amount = models.FloatField(blank=False)
    payment_due = models.DateField(blank=False)


class EventStatus(models.Model):
    status = models.BooleanField(default=False, unique=True)

    @classmethod
    def get_default_pk(cls):
        event_status, created = cls.objects.get_or_create(status=False)
        return event_status.pk

    class Meta:
        verbose_name_plural = 'Event status'


class Event(models.Model):
    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, related_name='events', blank=False
    )
    date_created = models.DateField(auto_now_add=True, blank=False)
    date_updated = models.DateField(auto_now_add=True, blank=False)
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False
    )
    event_status = models.ForeignKey(
        to=EventStatus,
        on_delete=models.CASCADE,
        default=EventStatus.get_default_pk,
    )
    attendees = models.IntegerField(blank=False)
    event_date = models.DateField(blank=False)
    notes = models.CharField(max_length=400, blank=True)
