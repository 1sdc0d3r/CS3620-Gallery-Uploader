from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views import View
from django.http import HttpResponseRedirect


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


class ImageDetailView(DetailView):
    template_name="gallery/image_view.html"
    model = Image
    context_object_name='img'

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        loaded_img = self.object
        request = self.request
        context["comment"] = request.session.get("comment", "")
        return context


class AddComment(View):
    def post(self, request):
        img_id = request.POST['img_id']
        request.session['comment_image'] = str(img_id)
        old = request.session['comment']
        old += f"{request.POST['comment']}, "
        request.session['comment']=old
        return HttpResponseRedirect("/" + img_id)
