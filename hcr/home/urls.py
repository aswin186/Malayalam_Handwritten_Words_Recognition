from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.upload_images, name="home"),
    path('output_file/<int:id>', views.output_files, name='out'),
    path('delete/<int:id>',views.clear_all,name='clear'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)