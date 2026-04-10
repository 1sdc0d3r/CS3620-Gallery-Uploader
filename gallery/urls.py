from django.urls import path

from . import views

urlpatterns = [
    path("", views.GalleryListView.as_view()),
    path("upload/", views.UploadImageFormView.as_view()),
    path("comment/", views.AddComment.as_view()),
    path("<int:pk>", views.ImageDetailView.as_view())
]
