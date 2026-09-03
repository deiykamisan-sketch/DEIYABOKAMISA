from django.http import JsonResponse
def status(request): return JsonResponse({'module':'whiteboard','status':'ready'})
