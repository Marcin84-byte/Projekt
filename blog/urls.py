from django.urls import path
from .views import (
    blog_post_detail_view,
    blog_post_update_view,
    blog_post_delete_view,
    blog_post_create_view,

)

urlpatterns = [

    path('blog-add/', blog_post_create_view, name='add_blog'),
    path('<str:slug>/', blog_post_detail_view,name="post_detail",),
    path('<str:slug>/edit/', blog_post_update_view, name='update'),
    path('<str:slug>/delete/', blog_post_delete_view),


]