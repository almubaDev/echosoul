from django import forms
from .models import Secreto

class SecretoForm(forms.ModelForm):
    class Meta:
        model = Secreto
        fields = ['tipo', 'contenido_texto', 'contenido_audio', 'idioma', 'publico']
        widgets = {
            'tipo': forms.RadioSelect(choices=Secreto.TIPO_CHOICES),
            'contenido_texto': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu secreto…'}),
            'contenido_audio': forms.ClearableFileInput(attrs={'accept': 'audio/*'}),
            'idioma': forms.Select(choices=[('es', 'Español'), ('en', 'English')]),
            'publico': forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        texto = cleaned_data.get('contenido_texto')
        audio = cleaned_data.get('contenido_audio')

        if tipo == 'texto' and not texto:
            self.add_error('contenido_texto', "Debes escribir un secreto.")
        elif tipo == 'audio' and not audio:
            self.add_error('contenido_audio', "Debes subir un archivo de audio.")
