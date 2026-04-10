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

    def get_queryset(self):
        tag_query = self.request.GET.get('tag')
        query_set=super().get_queryset()
        if not tag_query: return query_set
        # print(query)
        tags=tag_query.split(",")
        query_set = query_set.filter(tags__contains=tags[0])
        # print(query_set)
        # print(tags)
        return query_set

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["history"] = self.request.session.get('history')
        return context




class ImageDetailView(DetailView):
    template_name="gallery/image_view.html"
    model = Image
    context_object_name='img'


    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)

        request = self.request
        comments = request.session.get("comments")
        if not isinstance(comments, dict):
            comments = {}
        context["comments"] = comments
        img_pk = str(self.object.pk)
        if comments.get(img_pk):
            context["comments"] = [c.strip() for c in comments.get(img_pk).split(",")]
        else:
            context["comments"] = []

        history = request.session.get('history')

        if history is None: request.session['history']=f'{img_pk},'
        elif img_pk not in history:
            request.session['history']+=f'{img_pk},'

        context['history']=request.session.get('history')
        return context


class AddComment(View):
    def post(self, request):
        img_id = str(request.POST["img_id"])
        session_comments = request.session.get("comments") or {}
        if not isinstance(session_comments, dict):
            session_comments = {}

        new_comment = f"{request.POST['comment']},"
        if session_comments.get(img_id):
            session_comments[img_id] += new_comment
        else:
            session_comments[img_id] = new_comment
        request.session["comments"] = session_comments

        return HttpResponseRedirect("/" + img_id)
