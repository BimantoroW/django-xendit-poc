from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from . import services
from courses.models import Course

@require_POST
@login_required
def add_cart_item(request):
    course_id = request.POST.get('course_id')
    if not course_id:
        return JsonResponse({'status': 'error', 'message': 'Course ID is missing.'}, status=400)

    course = get_object_or_404(Course, id=course_id)
    item_created = services.add_item(request.user, course_id)
    cart_items, _ = services.get_cart_by_user(request.user)

    if item_created:
        message = f"'{course.title}' was added to your cart."
    else:
        message = f"'{course.title}' is already in your cart."

    return JsonResponse({
        'status': 'success',
        'message': message,
        'cart_item_count': cart_items.count()
    })