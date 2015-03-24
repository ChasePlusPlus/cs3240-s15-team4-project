from SecureWitness.models import File, User, Group, Key, Folder
from django.contrib import admin

# Register your models here.


class FileAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')


class GroupAdmin(admin.ModelAdmin):
    pass


class KeyAdmin(admin.ModelAdmin):
    pass


class FolderAdmin(admin.ModelAdmin):
    pass


admin.site.register(File, FileAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
