from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from users.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser', 'is_moderator')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_moderator')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_moderator', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_moderator'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])  # Убедимся, что пароль хэшируется
        super().save_model(request, obj, form, change)

    def is_moderator(self, obj):
        return obj.groups.filter(name='moderators').exists()
    is_moderator.boolean = True
    is_moderator.short_description = 'Is Moderator'


admin.site.unregister(Group)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count')

    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = 'Number of Users'


admin.site.register(Group, GroupAdmin)
