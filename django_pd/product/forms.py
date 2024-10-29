# forms.py
from django import forms

class DataForm(forms.Form):
    text_data = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Type your data here...',
             'class': 'form-control form-floating',  # Bootstrap classes
             'rows': '3'  # Optional: Set the number of rows for better display
        }),
        required=False
    )
    file_data = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'custom-file-input-class'
        }),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        text_data = cleaned_data.get('text_data')
        file_data = cleaned_data.get('file_data')

        if not text_data and not file_data:
            raise forms.ValidationError("Please enter data or upload a file.")
        
        return cleaned_data
