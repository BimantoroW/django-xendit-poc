from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from django.http import HttpResponseForbidden

@login_required
def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    if not is_enrolled:
        return HttpResponseForbidden("You are not enrolled in this course.")

    context = {
        'course': course
    }
    return render(request, 'courses/course-details.html', context)