
from django.db import models


# 1. STUDENT TABLE
class Student(models.Model):
    admission_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admission_number} - {self.name}"


# 2. BOOK TABLE
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    publisher = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


# 3. LIBRARY RECORD TABLE
class LibraryRecord(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="library_records"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        related_name="library_records"
    )
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )

    def __str__(self):
        return f"{self.student.name} - {self.book.title}"


# 4. MESS RECORD TABLE
class MessRecord(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="mess_records"
    )
    meal_date = models.DateField()
    meal_type = models.CharField(
        max_length=20,
        choices=[
            ("BREAKFAST", "Breakfast"),
            ("LUNCH", "Lunch"),
            ("DINNER", "Dinner"),
        ]
    )
    attended = models.BooleanField(default=True)
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("PAID", "Paid"),
            ("PENDING", "Pending"),
        ],
        default="PENDING"
    )

    def __str__(self):
        return f"{self.student.name} - {self.meal_type}"


# 5. GYM MEMBERSHIP TABLE
class GymMembership(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="gym_memberships"
    )
    membership_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    fee_amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.name} - {self.membership_type}"


# 6. GYM VISIT TABLE
class GymVisit(models.Model):
    membership = models.ForeignKey(
        GymMembership,
        on_delete=models.PROTECT,
        related_name="visits"
    )
    visit_date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.membership.student.name} - {self.visit_date}"
