
"""projet_muscu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
import muscu_site.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='muscu_site/login.html', redirect_authenticated_user=False),
         name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='muscu_site/login.html'), name='logout'),
    path('sessions/', muscu_site.views.sessions_list, name='sessions_list'),
    path('sessions/create/', muscu_site.views.create_session, name='create_session'),
    path('sessions/complete/<int:session_id>/', muscu_site.views.complete_session, name='complete_session'),
    path('sessions/complete/delete/<int:session_id>/', muscu_site.views.delete_session, name='delete_session'),
    path('sessions/summary/delete/<int:session_completed_id>/', muscu_site.views.delete_session_completed,
         name='delete_session_completed'),
    path('sessions/summary/<int:session_completed_id>/', muscu_site.views.session_summary, name='session_summary'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
