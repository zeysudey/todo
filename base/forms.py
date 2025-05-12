from django import forms
from .models import Task

# Reordering Form and View

class TaskForm(forms.ModelForm): # Task form
    class Meta: 
        model = Task 
        fields = ['title', 'description', 'complete', 'deadline', 'branch'] # Fields to be included in the form
        labels = { 
            'title': 'Başlık',
            'description': 'Açıklama',
            'complete': 'Tamamlandı mı?',
            'deadline': 'Son Tarih',
            'branch': 'Birim',
        }
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }
class PositionForm(forms.Form):
    position = forms.CharField()
    