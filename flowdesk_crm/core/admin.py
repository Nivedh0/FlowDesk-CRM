# Register your models here.
from django.contrib import admin
from .models import (
    Status,
    Department,
    Course,
    UserProfile,
    StudentEnquiry,
    FollowUp,
    Module,
    Topic,
    Batch,
    Student,
    Fee,
    FeeInstallment,
    Payment,
    Attendance,
    SessionUpdate,
    LeadActivity,
    LeadTask,
)
admin.site.register(Status)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(UserProfile)
admin.site.register(StudentEnquiry)
admin.site.register(Module)
admin.site.register(Topic)
admin.site.register(Batch)
admin.site.register(Student)
admin.site.register(Fee)
admin.site.register(FeeInstallment)
admin.site.register(Payment)
admin.site.register(Attendance)
admin.site.register(SessionUpdate)
admin.site.register(LeadActivity)
admin.site.register(LeadTask)
admin.site.register(FollowUp)   
