from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.hashers import make_password

User = get_user_model()


class RoleFilter(SimpleListFilter):
    title = 'Role'
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        return (
            ('superadmin', 'Superadmin'),
            ('admin', 'Admin'),
            ('intern', 'Intern'),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == 'superadmin':
            return queryset.filter(is_superuser=True)
        elif value == 'admin':
            return queryset.filter(is_staff=True, is_superuser=False)
        elif value == 'intern':
            return queryset.filter(is_staff=False, is_superuser=False)

        return queryset


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'get_role',
        'is_active',
        'date_joined',
    )

    search_fields = ('first_name', 'last_name', 'email')
    list_filter = (RoleFilter, 'is_active', 'position', 'department')
    list_per_page = 20

    # Все поля, включая readonly
    fields = ('email', 'password', 'first_name', 'last_name', 'position', 
              'department', 'is_active', 'is_staff', 'is_superuser',
              'date_joined', 'last_login')  # добавлены поля с датами
    
    # Поля только для чтения
    readonly_fields = ('date_joined', 'last_login')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(is_superuser=False)
        return qs

    def get_role(self, obj):
        if obj.is_superuser:
            return 'superadmin'
        elif obj.is_staff:
            return 'admin'
        return 'intern'

    get_role.short_description = 'Role'
    
    def save_model(self, request, obj, form, change):
        # Если пароль был изменен и не хеширован
        if 'password' in form.changed_data:
            if obj.password and not obj.password.startswith('pbkdf2_sha256$'):
                obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)