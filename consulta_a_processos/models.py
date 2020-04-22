from django.db import models
# Create your models here.
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField


#from django.contrib.postgres.fields import ArrayField

# Essa classe determina o que vai ser salvo na Database. Se houverem modificações, as migrations devem ser feitas
# Ao adicionar uma nova classe, antes das migrações, um valor default deve ser acrescentado.
 
class Processos(models.Model):
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classe = models.TextField()
    numero = models.TextField()
    descricao = models.TextField()
    incidente_id = models.TextField(default="id", blank=True)
    data_atualizacao = models.TextField(default="03/10/1995", blank=True)
    descricao_atualizacao = models.TextField(default="desc_at", blank=True, null=True)
    emails = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=8,
        ),
        size=8,
    )
    #emails = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    #emails_0 = models.TextField(default="globomonitoracao@gmail.com")
    #emails_1 = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    #emails_2 = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    #emails_3 = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    #emails_4 = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    #emails_5 = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    #emails_6 = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    #emails_7 = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    #emails_8 = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    #emails_9 = models.TextField(default="globomonitoracao@gmail.com", blank=True, null=True)
    url = models.TextField(default="url", blank = True)
    #created_date = models.DateTimeField(default=timezone.now)
    #published_date = models.DateTimeField(blank=True, null=True)
    #emails = MultiEmailField(null=True)
      

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.descricao

    def get_absolute_url(self):
        return reverse('processos_edit', kwargs={'pk': self.pk})


    #def get_queryset(self):
    #    return Processos.objects.all()