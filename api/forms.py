from django import forms 
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'passwd']
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

class ImageProcessingForm(forms.ModelForm):
    class Meta:
        model = ImageProcessing
        fields = ['mask_size', 'brightness']