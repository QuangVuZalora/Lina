import os
from base64 import b64encode

from django.shortcuts import render

from Lina.settings import STATIC_ROOT
from Slayer.ImageUploadForm import ImageUploadForm
from Slayer.models import ImageFile
from engine.visenze import Visenze

search_engine = Visenze()
def home(request):
    return render(request, "home.html", {})


def search(request):
    image_dir = os.path.join(STATIC_ROOT, 'images/')
    files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    images = []
    for image_file in files:
        f = open(image_file)
        encoded = b64encode(f.read())
        mime = "image/jpeg"
        image = dict()
        image['uri'] = "data:%s;base64,%s" % (mime, encoded)
        image['file'] = image_file
        images.append(image)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['image']:
                image_file = form.cleaned_data['image']
                image_obj = ImageFile()
                image_obj.image = image_file
                image_obj.save()
                image_url = image_obj.image.path
            else:
                image_url = form.cleaned_data['image_url']

            if image_file is None:
                return render(request, "result.html", {"error": "Please choose or upload an image.", 'images': images})
            gender = form.cleaned_data['gender']
            products = search_engine.search_image(image_url, gender)
            products = [{'url': link[0], 'image': link[1]} for sku, link in products.iteritems()]
            return render(request, 'result.html', {'products': products, 'images': images})
    return render(request, "result.html", {'images': images})


def get_image_from_url(form):
    if form.cleaned_data['image_url'] and os.path.isfile(form.cleaned_data['image_url']):
        return open(form.cleaned_data['image_url'])
    return None
