from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from users.forms import MyAuthForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/<username>/', user_views.profile, name='profile'),
    path('profile/edit', user_views.profile_editor, name='profile-editor'),
    path('register/', user_views.register, name='register'),
    path('users/follow/', user_views.user_follow, name='user_follow'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=MyAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('blog.urls')),
    path('market/', include('market.urls')),
    path('actions/', include('actions.urls')),
    path('messages/', include('messanger_system.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

