from django.forms import ModelForm
from django.forms.widgets import Textarea
from .models import *

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'created', 'like_count']
        widgets = {'content': Textarea(attrs={
                'class':'form-control',
                'rows':'3',
                'cols':'20',
                'placeholder':"Enter Text Here"
        })}