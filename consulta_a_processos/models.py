from django.db import models
# Create your models here.
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
#from django.contrib.postgres.fields import ArrayField
#from multi_email_field.fields import MultiEmailField


#from django.contrib.postgres.fields import ArrayField

# Essa classe determina o que vai ser salvo na Database. Se houverem modificações, as migrations devem ser feitas
# Ao adicionar uma nova classe, antes das migrações, um valor default deve ser acrescentado.
 
class Processos(models.Model):
	   # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    classe = models.TextField()
    numero = models.TextField()
    descricao = models.TextField()
    incidente_id = models.TextField(default="id", blank=True)
    data_atualizacao = models.TextField(default="03/10/1995", blank=True)
    descricao_atualizacao = models.TextField(default="desc_at", blank=True, null=True)
    emails = models.TextField(default="processosglobobsa@gmail.com", blank=True, null=True)
    url = models.TextField(default="url", blank = True)
      

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.descricao

    def get_absolute_url(self):
        return reverse('processos_edit', kwargs={'pk': self.pk})


    #def get_queryset(self):
    #    return Processos.objects.all()
