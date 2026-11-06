from django.contrib import admin
from .models import Student, StudentAccount, Faculty, FeedbackForm, Feedback


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("uid", "class_name", "subject", "has_login")
    search_fields = ("uid", "class_name", "subject")

    @admin.display(boolean=True, description="Login created")
    def has_login(self, obj):
        return hasattr(obj, "account")


@admin.register(StudentAccount)
class StudentAccountAdmin(admin.ModelAdmin):
    list_display = ("student", "user", "created_at")
    search_fields = ("student__uid", "user__email", "user__username")


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("faculty_id", "faculty_name", "mobile_no", "email_id")
    search_fields = ("faculty_id", "faculty_name", "email_id")


@admin.register(FeedbackForm)
class FeedbackFormAdmin(admin.ModelAdmin):
    list_display = ("feedback_form_id", "form_title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("feedback_form_id", "form_title")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("feedback_id", "student", "faculty", "rating", "feedback_date")
    list_filter = ("rating", "feedback_date", "faculty")
    search_fields = ("student__uid", "faculty__faculty_name", "feedback_message")
    readonly_fields = ("feedback_date",)
