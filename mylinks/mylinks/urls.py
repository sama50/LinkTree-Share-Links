from django.contrib import admin
from django.urls import path
from app.views import home,create_bio, bio_page, save_profile
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('create-bio',create_bio,name='create_bio'),
    path('bio-page/<str:id>/',bio_page),
    path('save-profile/',save_profile, name='save_profile'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
