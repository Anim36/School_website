from .models import SchoolInfo

def school_info(request):
    try:
        school = SchoolInfo.objects.first()
    except SchoolInfo.DoesNotExist:
        school = None
    return {'school_info': school}