from django.db import models

# Create your models here.
from django.db import models


from django.db import models
from django.contrib.auth.models import User

class Documento(models.Model):
    nombre = models.CharField(max_length=100)
    texto = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre