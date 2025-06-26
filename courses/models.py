from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    price = models.IntegerField()
    image_path = models.CharField(max_length=256, null=True, blank=True)

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)