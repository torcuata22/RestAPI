from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import UserChangeForm, UserCreationForm
from .models import User

# Get the existing UserAdmin instance
user_admin = admin.site._registry.get(User)

# If it exists, modify it
if user_admin:
    user_admin.fieldsets = (
        (_("Login Credentials"), {"fields":("email", "password")}),
        (_("Personal Info"), {"fields":("first_name", "last_name")}),
        (_("Permissions and Groups"), {"fields":("is_active", "is_staff", "is_superuser")}),
        (_("Important Dates"), {"fields":("last_login", "date_joined")}),
    )

    user_admin.add_fieldsets = (
        (None, {
            "classes":("wide",),
            "fields":("email", "first_name", "last_name", "password1", "password2"),
        })
    )

# Register the UserAdmin if not already registered
else:
    class UserAdmin(BaseUserAdmin):
        ordering = ["email"]
        form = UserChangeForm
        add_form = UserCreationForm
        model = User

        list_display = ["pkid", "id", "email", "first_name", "last_name", "is_staff", "is_active" ]
        list_display_links = ["pkid", "id", "email"]
        list_filter = [ "email", "is_staff", "is_active"]
        fieldsets = (
            (_("Login Credentials"), {"fields":("email", "password")}),
            (_("Personal Info"), {"fields":("first_name", "last_name")}),
            (_("Permissions and Groups"), {"fields":("is_active", "is_staff", "is_superuser")}),
            (_("Important Dates"), {"fields":("last_login", "date_joined")}),
        )

        add_fieldsets = (
            (None, {
                "classes":("wide",),
                "fields":("email", "first_name", "last_name", "password1", "password2"),
            })
        )

        search_fields = ["email", "first_name", "last_name"]

    admin.site.register(User, UserAdmin)
