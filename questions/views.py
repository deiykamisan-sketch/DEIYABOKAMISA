from django.http import JsonResponse
def status(request): return JsonResponse({'module':'questions','status':'ready'})
