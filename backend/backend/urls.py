"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, re_path
from stocks import views
from stocks.views import FrontendAppView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/analysis/', views.stock_analysis),
    path('api/save-portfolio/', views.save_portfolio),


    # 🧠 React frontend fallback (excluding admin and api paths)
    re_path(r'^(?!admin/|api/).*$', FrontendAppView.as_view(), name='home'),
]