from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('댓글',)

        widgets = {
            '댓글': forms.Textarea(attrs={ 'rows': 7, 'cols': 93})
        }