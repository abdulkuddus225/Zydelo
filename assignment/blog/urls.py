from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.register, name="register"),
    path('bloghome/', views.bloghome, name="bloghome"),
    path('login/', views.userlogin, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('myblog/',  views.myblog, name='myblog'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('myblog/delete/<int:id>', views.delete_blog, name='delete'),
    path('myblog/edit/<int:id>', views.edit_blog, name='edit')
    
]
