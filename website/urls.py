from django.urls import path
from . import views
from django.contrib.auth import views as authViews
urlpatterns = [
    # path('create_database', views.cr_db, name="create"),
    path('', views.main, name="home_page"),
    path('addtitle/<pk>/', views.add_vie, name="page_add"),
    path('exit/', authViews.LogoutView.as_view(next_page='/'), name='exit'),
]
