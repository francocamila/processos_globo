from django import forms
from .models import Processos
 

class ProcessosForm(forms.ModelForm):    

    class Meta:
        model = Processos
        fields = ('classe', 'numero', 'descricao', 'emails',)