from base64 import b64encode

from django.http import HttpResponseForbidden
from django.shortcuts import render, render_to_response

from Slayer.ImageUploadForm import ImageUploadForm


def home(request):
    return render(request, "home.html", {})


def search(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            encoded = b64encode(image_file.read())
            mime = "image/jpeg"
            uri = "data:%s;base64,%s" % (mime, encoded)
            return render_to_response('search.html', {'image_url': uri})
    return HttpResponseForbidden('allowed only via POST')


