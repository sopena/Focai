from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subjects, UserSubjects


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["email", "username", "first_name", "last_name", "is_active", "is_staff"]
    search_fields = ["email", "username", "first_name"]
    ordering = ["email"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "last_name")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Datas importantes", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2"),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Subjects)
admin.site.register(UserSubjects)
