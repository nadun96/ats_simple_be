from django.http import HttpResponse, JsonResponse

def home(request):
    return HttpResponse("Welcome to the Application Microservice!")

def health_check(request):
    return JsonResponse({"status": "healthy"})
