from django.http import JsonResponse
def status(request): return JsonResponse({'module':'pen_tracking','status':'ready'})
