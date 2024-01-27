from django.contrib import admin

from contact import models


@admin.register(models.ContactModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "phone", "show"]
    ordering = ["-id"]
    list_filter = ["created_at"]
    list_per_page = 10
    list_max_show_all = 200
    list_editable = ["show"]


@admin.register(models.CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["-id"]
