from django.http import JsonResponse
def status(request): return JsonResponse({'module':'recording','status':'ready'})
