"""
URL configuration for djangoTeste project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name="delete_comment"),
    path('post/<int:post_id>/comment/', views.add_new_comment, name='post_comment'),
    path('posts/', views.list_posts, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
