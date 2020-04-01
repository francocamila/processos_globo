from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone


class Processos(models.Model):
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classe = models.TextField()
    numero = models.TextField()
    descricao = models.TextField()
    incidente_id = models.TextField()
    data_atualizacao = models.TextField()
    descricao_atualizacao = models.TextField()
    emails = models.EmailField()
    #created_date = models.DateTimeField(default=timezone.now)
    #published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.descricao