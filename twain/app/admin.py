from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm
from .models import *

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'is_admin','is_verified',"is_active","username1")
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password','username1')}),
        ('Personal info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('is_admin','is_verified',"is_active","is_online")}),
        ('Profile Type',{'fields':('is_costomer','is_dealer')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username1', 'first_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','is_verified')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

@admin.register(OTPModel)
class OTPAdmin(admin.ModelAdmin):
    list_display= ['user','otp']


@admin.register(DealerProfileModel)
class DealerProfileAdmin(admin.ModelAdmin):
    list_display= ['user']
    # ,'company_name'

@admin.register(CostomerProfileModel)
class CostomerAdmin(admin.ModelAdmin):
    list_display= ['user','gender','address','profile_picture']

@admin.register(JobTypeModel)
class JobTypeAdmin(admin.ModelAdmin):
    list_display= ['job_type_title','job_type_desc']

@admin.register(JobCategoryModel)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display= ['category_title','category_desc']


@admin.register(PostjobModel)
class PostjobAdmin(admin.ModelAdmin):
    list_display= ['dealer','job_title']

@admin.register(ApplyForJobModel)
class ApplyForJobAdmin(admin.ModelAdmin):
    list_display= ['id','costomer','applied_job','applied_job_id','dealer']

@admin.register(SkillModel)
class SkillAdmin(admin.ModelAdmin):
    list_display= ['skill_title']

@admin.register(BidAmountModel)
class BidAmountAdmin(admin.ModelAdmin):
    list_display= ['bid_amount','is_accepted','job_id']
    
@admin.register(Payment)
class BidPaymentAdmin(admin.ModelAdmin):
    list_display= ['dealer','order_id','payment_id','payment_signature','amount','job']

@admin.register(ProjectBillingModel)
class ProjectBillingModelAdmin(admin.ModelAdmin):
    list_display= ['user','id']
    list_filter=['user']
    
admin.site.register(BillingReport)
admin.site.register(Comment)
admin.site.register(AccountDetailsModel)