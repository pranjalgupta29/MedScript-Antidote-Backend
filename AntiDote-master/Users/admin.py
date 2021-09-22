from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User,Patient,Doctor,Reports,Treatment,Disease,Specialization,Symptom,QnA

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',"is_doctor",'is_patient')
    list_filter = ('email', 'is_staff', 'is_active',"is_doctor",'is_patient')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',"is_doctor",'is_patient')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',"is_doctor",'is_patient', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class ReportAdmin(admin.ModelAdmin):
    filter_horizontal = ("Doctors",)

class SymptomAdmin(admin.ModelAdmin):
    filter_horizontal = ("SymptomList",)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Reports,ReportAdmin)
admin.site.register(Treatment,SymptomAdmin)
admin.site.register(Specialization)
admin.site.register(Disease)
admin.site.register(Symptom)
admin.site.register(QnA)