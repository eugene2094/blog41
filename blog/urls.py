from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import MyLogoutView

urlpatterns = [
    path("", views.index, name="main"),
    path("post/<str:name>", views.post, name="post"),
    path("contacts", views.contact, name="contacts"),
    path('category/<str:c>', views.category, name="category"),
    path('search', views.search, name='search'),
    path('create', views.create, name='create'),
    path('login', LoginView.as_view(), name="blog_login"),
    path('logout', MyLogoutView.as_view(), name="blog_logout"),
    path('profile',views.profile,name="profile"),
    path("update-profile",views.update_profile,name="update_profile"),
    path("registration",views.registration,name="registration")
]
