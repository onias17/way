from django.urls import path, include
from . import views
from django.contrib import admin 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),

    ## PROFILE URLS
    path('profiles/index/', views.profiles_index, name="profiles_index"),
    path('profiles/new/', views.new_profile, name="new_profile"),
    path('profiles/<slug:slug>/', views.profiles_detail, name="detail"),
    path('profiles/<slug:slug>/edit/', views.profiles_edit, name="edit"),

    ##POST URLS
    path('cities/<city_id>/add_post', views.add_citypost, name='add_citypost'),
    path('profiles/<slug:slug>/add_post/', views.add_post, name="add_post"),
    path('posts/<int:post_id>/', views.posts_detail, name ="postdetail"),
    path('posts/<int:post_id>/edit', views.post_edit, name="postedit"),
    path('posts/<int:post_id>/delete', views.post_delete, name="deletepost"),
    path('posts/<int:post_id>/add_comment', views.add_comment, name="add_comment"),

    ##CITY URLS
    path('cities/new', views.add_city, name="add_city"),
    path('cities/index', views.city_index, name="city_index"),
    path('cities/<slug:slug>/', views.city_detail, name="citydetail"),
    ##SIGN UP URL
    path('accounts/signup', views.signup, name='signup'),
    ##DELETE COMMENT
    path('comments/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
    ##EMAIL PATH
    path('success', views.success, name = 'success')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)