from django import forms
from .models import Article

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'pdf_url']