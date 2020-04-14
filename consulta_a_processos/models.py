from django.db import models
# Create your models here.
from django.conf import settings
from django.utils import timezone

# Essa classe determina o que vai ser salvo na Database. Se houverem modificações, as migrations devem ser feitas
# Ao adicionar uma nova classe, antes das migrações, um valor default deve ser acrescentado.
 
class Processos(models.Model):
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classe = models.TextField()
    numero = models.TextField()
    descricao = models.TextField()
    incidente_id = models.TextField(default="id", blank=True)
    data_atualizacao = models.TextField(default="14/04/2020", blank=True)
    descricao_atualizacao = models.TextField(default="desc_at", blank=True, null=True)
    emails = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    url = models.TextField(default="url", blank = True)
    #created_date = models.DateTimeField(default=timezone.now)
    #published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.descricao


    #def get_queryset(self):
    #    return Processos.objects.all()