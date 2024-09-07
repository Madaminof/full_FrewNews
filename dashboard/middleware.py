from django.shortcuts import render

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Faqat 404 xato bo'lganda maxsus sahifa qaytariladi
        if response.status_code == 404:
            return render(request, '404.html', status=404)
        return response
