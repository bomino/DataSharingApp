from django import forms
from .models import DataFile

class DataFileUploadForm(forms.ModelForm):
    class Meta:
        model = DataFile
        fields = ['file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError('File size must be under 10MB')
            if not file.name.endswith(('.csv', '.xlsx', '.xls')):
                raise forms.ValidationError('Only CSV and Excel files are allowed')
        return file