from django.urls import path
from . import views

urlpatterns = [
    path('shows', views.index, name = "shows"),
    path('shows/<int:tv_show_id>', views.show, name = "tv_show"),
    path('shows/<int:tv_show_id>/edit', views.edit, name = "edit"),
    path('shows/<int:tv_show_id>/destroy', views.destroy, name = "destroy"),
    path('shows/<int:tv_show_id>/update', views.update, name = "update"),
    path('shows/new', views.new_show, name = "new_show"),
    path('add_show', views.add_show, name = "add_show"),
]
