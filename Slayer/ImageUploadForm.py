from django import forms


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField(required=False)
    image_url = forms.CharField(required=False)
