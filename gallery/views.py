from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import Image

class UploadImageFormView(CreateView):
    template_name = 'gallery/image_form.html'
    model = Image
    fields = '__all__'
    success_url = '/'


class GalleryListView(ListView):
    template_name = 'gallery/gallery.html'
    model = Image
    context_object_name = 'images'
