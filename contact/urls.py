from django.urls import path

from . import views

app_name = "contact"

urlpatterns = [
    path("search/", views.search, name="search"),
    path("", views.index, name="index"),
    # contact
    path("contact/<int:contact_id>/detail/", views.contact, name="contact"),
    path("contact/<int:contact_id>/update/", views.update, name="update"),
    path("contact/<int:contact_id>/delete/", views.delete, name="delete"),
    path("contact/create/", views.create, name="create"),
    # user
    path("user/register/", views.register, name="register"),
    path("user/update/", views.update_user, name="update-user"),
    path("user/login/", views.auth_view, name="login"),
    path("user/logout/", views.logout_view, name="logout"),
]
