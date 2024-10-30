from django.forms import ModelForm
from .models import UpImages

class ImagesForm(ModelForm):
    class Meta:
        model = UpImages
        fields = '__all__'