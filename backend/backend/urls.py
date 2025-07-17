from django.contrib import admin
from django.urls import path
from stocks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/analysis/', views.stock_analysis),
    path('api/save-portfolio/', views.save_portfolio),
]
