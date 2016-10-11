import os
from base64 import b64encode, b64decode
from django.http import HttpResponse
from django.shortcuts import render
import json
from Lina.settings import STATIC_ROOT, BASE_DIR
from Slayer.ImageUploadForm import ImageUploadForm
from Slayer.models import ImageFile
from engine.visenze import Visenze
from django.views.decorators.csrf import csrf_exempt
search_engine = Visenze()
from django.core.files.base import ContentFile
from django.core.files import File
def home(request):
    return render(request, "home.html", {})

@csrf_exempt
def mobile_search(request):
    print dir(request)
    products = []
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        data = b64decode(request.POST.get('image_base64'))
        file_name = request.POST.get('file_name')
        image_dir = os.path.join(BASE_DIR, 'images/')
        file_dir = image_dir + file_name
        print file_dir
        fh = open(file_dir, "wb")
        fh.write(data)
        fh.close()
        print 'ack'
        gender = request.POST.get('gender')
        products = search_engine.search_image(file_dir, gender)
        products = [{'url': link[0], 'image': link[1]} for sku, link in products.iteritems()]
        # print products
    return HttpResponse(json.dumps(products), content_type="application/json")

def search(request):
    image_dir = os.path.join(STATIC_ROOT, 'images/')
    files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    images = []
    for image_file in files:
        f = open(os.path.join(image_dir, image_file))
        encoded = b64encode(f.read())
        mime = "image/jpeg"
        image = dict()
        image['uri'] = "data:%s;base64,%s" % (mime, encoded)
        image['file'] = image_file
        images.append(image)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            relative_url = None
            host_url = None
            if form.cleaned_data['image']:
                image_file = form.cleaned_data['image']
                image_obj = ImageFile()
                image_obj.image = image_file
                image_obj.save()
                image_url = image_obj.image.path
                host_url = request.build_absolute_uri(image_obj.image.url)
            else:
                relative_url = "images/" + form.cleaned_data['image_url']
                image_url = os.path.join(image_dir, form.cleaned_data['image_url'])

            if image_url is None:
                return render(request, "result.html", {"error": "Please choose or upload an image.", 'images': images})
            gender = form.cleaned_data['gender']
            print image_url
            products = search_engine.search_image(image_url, gender)
            products = [{'url': link[0], 'image': link[1]} for sku, link in products.iteritems()]
            return render(request, 'result.html',
                          {'products': products, 'images': images, 'input_url': relative_url, 'host_url': host_url})
    return render(request, "result.html", {'images': images})


def get_image_from_url(form):
    if form.cleaned_data['image_url'] and os.path.isfile(form.cleaned_data['image_url']):
        return open(form.cleaned_data['image_url'])
    return None
