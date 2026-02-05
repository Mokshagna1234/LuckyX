"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from users.views import login_view, logout_view, signup_view, account_page
from draw.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH
    path('login/', login_view),
    path('logout/', logout_view),
    path('signup/', signup_view),

    # HOME
    path('', dashboard),

    # APPS
    
    path('draw/', include('draw.urls')),
    path('wallet/', include('wallet.urls')),
    path('account/', include('users.urls')),

    #
]
