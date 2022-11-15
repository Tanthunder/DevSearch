
from django.contrib import admin
from django.urls import path , include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
import debug_toolbar 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('', include('users.urls')),
    path('api/', include('api.urls')),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = 'reset_password.html'), name='reset_password'), #user submits email for reset
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name ='reset_password_sent.html'), name='password_reset_done'), #email sent message
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name ='reset.html'), name='password_reset_confirm'), #email with link and reset instruction
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name ='reset_password_complete.html'), name='password_reset_complete'), #password successfully reset message
    path('debug/', include('debug_toolbar.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)