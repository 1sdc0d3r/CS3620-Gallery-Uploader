from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views import View
from django.http import HttpResponseRedirect
from .models import Image
from os.path import basename


class UploadImageFormView(CreateView):
    template_name = 'gallery/image_form.html'
    model = Image
    fields = '__all__'
    success_url = '/'
    # print(self.request)
    # def post(self,req):
    #     # print("post img: ", req)
    #     return HttpResponseRedirect("/")
    def form_valid(self, form):
        img_name = form.cleaned_data.get('img').name.replace(" ", "_")
        recent_session=self.request.session.get(f"recent") or []
        # if not isinstance(recent_session, list):
        #     self.request.session['recent'] = []
        if img_name not in recent_session:
            self.request.session['recent'] = [*recent_session, img_name]

        return super().form_valid(form)



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

class RecentListView(ListView):
    template_name = 'gallery/recent.html'
    model = Image
    context_object_name = 'images'

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["recent"] = self.request.session.get('recent')
        return context

    def get_queryset(self):
        query_set=super().get_queryset()
        # print("before", query_set)
        recents = self.request.session.get('recent') or []
        # print("last: ", recents[-1], "|")
        # img1=query_set[len(query_set)-1].img.name
        # print("img1: ",img1[img1.find('/')+1:], "|")
        # print(img1 in recents)

        query_set =[img for img in query_set if img.img.name[img.img.name.find("/")+1:] in recents]

        return query_set
