from django.urls import path
from . import views


urlpatterns = [
    # path('create_database', views.cr_db, name="create"),
    path('', views.main, name="home_page"),
    path('addtitle', views.add_vie, name="page_add"),

]