from django.contrib import admin
from accounts.models import Student, StudentMark, Subject, ReportCardID

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'first_name', 'last_name', 'class_name', 'father_name', 'mother_name']
    fieldsets = (
        (None, {'fields': ('roll_number',)}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('User Profile', {
            'classes': ('wide',),
            'fields': ('email', 'father_name', 'mother_name', 'class_name')
        }),
    )

admin.site.register(Student, UserAdmin)
admin.site.register(StudentMark)
admin.site.register(Subject)
admin.site.register(ReportCardID)