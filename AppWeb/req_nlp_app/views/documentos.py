from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
import json
import re
from django.contrib.auth.decorators import login_required

from req_nlp_app.models import Documento

@login_required
def inicio(request):
    documentos = Documento.objects.filter(usuario=request.user)
    return render(request, 'req_nlp_app/inicio.html', {'documentos': documentos})



@login_required
def lista_documentos(request):
    documentos = Documento.objects.filter(usuario=request.user)
    return render(request, 'req_nlp_app/inicio.html', {'documentos': documentos})

@login_required
def api_documentos(request):
    documentos = Documento.objects.filter(usuario=request.user).values('id', 'nombre')
    return JsonResponse(list(documentos), safe=False)


@login_required
@csrf_exempt
def nuevo_documento(request):
    if request.method == 'POST':
        # Buscar documentos con nombres similares del usuario
        documentos = Documento.objects.filter(usuario=request.user, nombre__startswith="Nuevo Documento")

        # Obtener el mayor número
        numeros = []
        for doc in documentos:
            match = re.search(r"Nuevo Documento (\d+)", doc.nombre)
            if match:
                numeros.append(int(match.group(1)))

        siguiente_numero = max(numeros, default=0) + 1
        nombre = f"Nuevo Documento {siguiente_numero}"

        doc = Documento.objects.create(usuario=request.user, nombre=nombre, texto='')
        return JsonResponse({'id': doc.id, 'nombre': doc.nombre})

@login_required
@csrf_exempt
def renombrar_documento(request, documento_id): 
    if request.method == 'POST':
        data = json.loads(request.body)
        nuevo_nombre = data.get('nombre')

        if not nuevo_nombre:
            return JsonResponse({"success": False, "error": "Nombre vacío"}, status=400)

        try:
            doc = Documento.objects.get(id=documento_id, usuario=request.user)
            doc.nombre = nuevo_nombre
            doc.save()
            return JsonResponse({"success": True, "nuevo_nombre": doc.nombre})
        except Documento.DoesNotExist:
            return JsonResponse({"success": False, "error": "Documento no encontrado"}, status=404)
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)


@login_required
@csrf_exempt
def guardar_documento(request, documento_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            texto = data.get('texto', '')
            doc = Documento.objects.get(id=documento_id, usuario=request.user)
            doc.texto = texto  
            doc.save()
            return JsonResponse({'status': 'ok'})
        except Documento.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Documento no encontrado'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


@login_required
def obtener_contenido_documento(request, documento_id):
    if request.method == 'GET':
        doc = get_object_or_404(Documento, id=documento_id, usuario=request.user)
        return JsonResponse({'texto': doc.texto})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

@csrf_exempt
@login_required
def eliminar_documento(request, documento_id):
    if request.method == 'POST':
        try:
            doc = Documento.objects.get(id=documento_id, usuario=request.user)
            doc.delete()
            return JsonResponse({'status': 'ok'})
        except Documento.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Documento no encontrado'}, status=404)