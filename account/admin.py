from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Profile,CustomUser,FeedbackModel

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username","email","total_scores","rank")
    list_filter = ("rank",)
    save_on_top = True

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user","get_image","is_baned",)
    readonly_fields = ("get_image",)

    def get_image(self,obj):
        return mark_safe(f'<img src = {obj.avatar.url} width = "80px" height = "80px">')

    def is_baned(self,obj):
        if obj.is_baned == False:
            readonly_fields = ("ban_time",)

    get_image.short_description = "Profile image"


@admin.register(FeedbackModel)
class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = ("mail_subject","mail_text","user","send_time",)
    readonly_fields = ("mail_subject","mail_text","send_time")
