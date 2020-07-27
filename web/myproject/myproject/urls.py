"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from myapp.views import mainpage, register, userfile, foruser, UserLoginView, signup, polifile, forpoli, alldata, error
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', mainpage, name="mainpage"),
    path('admin/', admin.site.urls),
    path('register/', register, name="register"),
    path('userfile/', userfile, name="userfile"),
    path('foruser/', foruser, name="foruser"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('signup/', signup, name="signup"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('polifile/', polifile, name="polifile"),
    path('forpoli/', forpoli, name="forpoli"),
    path('alldata/', alldata, name="alldata"),
    path('error/', error, name="error"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)