from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('<int:course_id>/', views.view_course, name='details'),
]