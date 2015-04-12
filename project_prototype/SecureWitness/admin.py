from SecureWitness.models import File, UserProfile, Group, Key, Folder, Request
from django.contrib import admin

# Register your models here.


class FileAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    #list_display = ('user.first_name', 'user.last_name', 'user.email')
    pass


class GroupAdmin(admin.ModelAdmin):
    pass


class KeyAdmin(admin.ModelAdmin):
    pass


class FolderAdmin(admin.ModelAdmin):
    pass


class RequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(File, FileAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Request, RequestAdmin)
