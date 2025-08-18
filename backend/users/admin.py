from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, GeneralDoctorProfile, NurseProfile, PatientProfile


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model.
    """
    model = User
    # The forms to be used in add and change admin views
    # We customize the fieldsets to use 'email' instead of 'username'.

    # Fields to display in the user list view
    list_display = ("email", "full_name", "role", "is_staff", "is_active", "is_verified")
    list_filter = ("role", "is_staff", "is_active", "groups")
    search_fields = ("email", "full_name")
    ordering = ("email",)

    # The fields to be used in displaying the User model on the change form
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "role", "date_of_birth", "gender")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined", "updated_at")}),
    )

    # The fields to be used when creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "password2", "full_name", "role"),
            },
        ),
    )

    # Make auto-managed fields readonly
    readonly_fields = ("date_joined", "last_login", "updated_at")


# Register your custom user model with the custom admin class
admin.site.register(User, CustomUserAdmin)

# Register other profile models from the 'users' app
admin.site.register(GeneralDoctorProfile)
admin.site.register(NurseProfile)
admin.site.register(PatientProfile)