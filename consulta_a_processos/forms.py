from django import forms
from .models import Processos
 

class ProcessosForm(forms.ModelForm):    

    class Meta:
        model = Processos
        fields = ('classe', 'numero', 'descricao', 'incidente_id', 'data_atualizacao', 'descricao_atualizacao', 'emails',)