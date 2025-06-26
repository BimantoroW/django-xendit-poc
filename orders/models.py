from django.db import models
from django.conf import settings
from courses.models import Course

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING'
        PAID = 'PAID'
        EXPIRED = 'EXPIRED'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=OrderStatus, default=OrderStatus.PENDING)
    total_amount = models.IntegerField()

    xendit_invoice_id = models.CharField(max_length=255)
    xendit_invoice_url = models.URLField(max_length=1024)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.IntegerField()
