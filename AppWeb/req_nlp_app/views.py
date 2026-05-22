import os
from django.http import JsonResponse
from django.shortcuts import render

def config(request):
    backend_url = os.getenv("INVERTIR_TEXTO_API_URL", "http://localhost:8000")
    return JsonResponse({"backend_url": backend_url})
