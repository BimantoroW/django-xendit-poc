from django.shortcuts import render
from courses.models import Course, Enrollment

def home(request):
    enrolled_courses = []
    
    # Only show enrolled courses if the user is logged in
    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
        enrolled_courses = [enrollment.course for enrollment in enrollments]

    all_courses = Course.objects.all()

    # Find the courses that are available for the user to enroll in
    enrolled_course_ids = [course.id for course in enrolled_courses]
    available_courses = all_courses.exclude(id__in=enrolled_course_ids)

    context = {
        'enrolled_courses': enrolled_courses,
        'available_courses': available_courses,
    }
    
    return render(request, 'core/home.html', context)
