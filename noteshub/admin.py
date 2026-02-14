from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Notes
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # ✅ SAFE: fields that always exist
    list_display = ('display_name', 'is_teacher', 'is_student', 'is_active')
    list_filter = ('is_teacher', 'is_student', 'is_active')
    search_fields = ('roll_no', 'full_name')
    ordering = ('id',)   # ✅ safest ordering

    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('roll_no', 'full_name', 'dob')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_teacher', 'is_student'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'roll_no',
                'full_name',
                'dob',
                'password1',
                'password2',
                'is_teacher',
                'is_student',
                'is_active',
            ),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')

    # ✅ Custom safe display
    def display_name(self, obj):
        return obj.roll_no or obj.full_name or "User"

    display_name.short_description = "User"


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Notes)
