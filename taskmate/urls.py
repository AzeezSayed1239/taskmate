from django.contrib import admin
from django.urls import path,include
from todolist import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('todolist/', include('todolist.urls')),
    path('account/', include('users_app.urls')),
    path('contactus',views.contactus, name='contactus'),
    path('aboutus',views.aboutus, name='aboutus'),
]
