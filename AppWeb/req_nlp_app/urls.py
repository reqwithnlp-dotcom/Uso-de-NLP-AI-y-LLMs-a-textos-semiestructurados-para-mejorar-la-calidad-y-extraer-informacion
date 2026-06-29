from django.urls import path
from django.contrib.auth import views as auth_views

from req_nlp_app.views.documentos import obtener_contenido_documento


from .views import (
    inicio,
    login_view,
    logout_view, 
    signup_view,
    nuevo_documento,
    renombrar_documento,
    guardar_documento,
    obtener_contenido_documento,
    eliminar_documento,
    api_documentos,
    lista_documentos, 
    
)

urlpatterns = [
    path('', inicio, name='inicio'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('nuevo_documento/', nuevo_documento, name='nuevo_documento'),
    path('renombrar_documento/<int:documento_id>/', renombrar_documento, name='renombrar_documento'),
    path('guardar_documento/<int:documento_id>/', guardar_documento, name='guardar_documento'),
    path('obtener_contenido_documento/<int:documento_id>/', obtener_contenido_documento, name='obtener_contenido_documento'),
    path('eliminar_documento/<int:documento_id>/', eliminar_documento, name='eliminar_documento'),
    path('api/documentos/', api_documentos, name='api_documentos'),
]

