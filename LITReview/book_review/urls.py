from django.urls import path, re_path
from . import views

app_name = "book_review"
urlpatterns = [
    path("", views.flux, name="flux"),
    path("posts", views.posts, name="posts"),
    path("abonnements", views.abonnements, name="abonnements"),
    re_path(r"^crea_ticket(?:/(?P<ticket_id>[0-9]+)/)?$", views.crea_ticket, name="crea_ticket"),
    path("crea_review", views.crea_review, name="crea_review"),
    path("reply_ticket/<ticket_id>", views.reply_ticket, name="reply_ticket"),
    
]
