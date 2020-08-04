from django.urls import path

from . import views

import random
from . import util

rand = random.choice(util.list_entries())

urlpatterns = [
    path("", views.index, name="index"),
    path("random",views.randompage, name="randompage"),
    path("addentry", views.addentry, name="addentry"),
    path("<str:entry>", views.getent, name="getent"),
	path("<str:entry>/editent", views.editentry, name="editentry")

]
