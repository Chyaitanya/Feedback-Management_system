
from django.contrib import admin
from .models import (
    Student,
    Book,
    LibraryRecord,
    MessRecord,
    GymMembership,
    GymVisit,
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "admission_number",
        "name",
        "class_name",
        "phone",
        "email",
        "address",
        "date_of_birth",
        "created_at",
    )
    search_fields = ("admission_number", "name", "phone", "email")
    list_filter = ("class_name", "created_at")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "isbn",
        "total_copies",
        "publisher",
    )
    search_fields = ("title", "author", "isbn", "publisher")


@admin.register(LibraryRecord)
class LibraryRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "book",
        "issue_date",
        "due_date",
        "return_date",
        "fine_amount",
    )
    search_fields = (
        "student__name",
        "student__admission_number",
        "book__title",
    )
    list_filter = ("issue_date", "due_date", "return_date")


@admin.register(MessRecord)
class MessRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "meal_date",
        "meal_type",
        "attended",
        "amount",
        "payment_status",
    )
    search_fields = ("student__name", "student__admission_number")
    list_filter = ("meal_type", "attended", "payment_status", "meal_date")


@admin.register(GymMembership)
class GymMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "membership_type",
        "start_date",
        "end_date",
        "fee_amount",
        "active",
    )
    search_fields = ("student__name", "student__admission_number")
    list_filter = ("membership_type", "active", "start_date", "end_date")


@admin.register(GymVisit)
class GymVisitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "membership",
        "visit_date",
        "check_in_time",
        "duration_minutes",
    )
    search_fields = (
        "membership__student__name",
        "membership__student__admission_number",
    )
    list_filter = ("visit_date",)
