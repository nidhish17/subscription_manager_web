from django.urls import path
from . import views



urlpatterns = [
   path("", views.home, name= "homepage"),
   path("login/", views.login_page, name= "login"),
   path("logout/", views.logout_user, name= "logout"),
   path("add_category", views.add_category, name= "add_category"),
   path("populate_category/", views.populate_categories, name= "populate_category"),
   path("delete_channel/<int:id>", views.delete_channel, name= "delete_channel"),
   path("delete_category/<int:id>", views.delete_category, name= "delete_category"),
]