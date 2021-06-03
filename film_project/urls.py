from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LoginView
from website.views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='singup'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    # path('', include('django.contrib.auth.urls')),
]