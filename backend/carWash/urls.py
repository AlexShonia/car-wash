from django.utils import path

from . import views

app_name = "carWash"
urlpatterns = [path("", views.indexView, name="index")]
