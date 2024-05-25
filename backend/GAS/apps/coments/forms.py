from django import forms
from .models import Comment

class FileCommentForm(forms.ModelForm):
    document = forms.FileField(required=False)
    
    class Meta:
        model = Comment
        fields = ['comment_text', 'document']