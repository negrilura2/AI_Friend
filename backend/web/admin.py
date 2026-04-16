from django.contrib import admin
from web.models.user import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",) #逗号不能删，因为要是列表，这样管理员那里点击搜索会分页。不加会是下拉框，用户太多会卡死。

# Register your models here.
