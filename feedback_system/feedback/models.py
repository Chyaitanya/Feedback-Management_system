from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    uid = models.CharField(max_length=30, primary_key=True, verbose_name="Student UID")
    class_name = models.CharField(max_length=40, verbose_name="Class / Standard")
    subject = models.CharField(max_length=100)

    class Meta:
        ordering = ["uid"]

    def __str__(self):
        return f"{self.uid} — {self.class_name} ({self.subject})"


class StudentAccount(models.Model):
    """Connects a Django login account to one pre-registered student record."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_account"
    )
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, related_name="account"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["student__uid"]

    def __str__(self):
        return f"{self.student.uid} student account"


class Faculty(models.Model):
    faculty_id = models.CharField(max_length=30, primary_key=True)
    faculty_name = models.CharField(max_length=120)
    mobile_no = models.CharField(max_length=15, blank=True)
    email_id = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["faculty_name"]
        verbose_name_plural = "Faculty"

    def __str__(self):
        return f"{self.faculty_name} ({self.faculty_id})"


class FeedbackForm(models.Model):
    feedback_form_id = models.CharField(max_length=30, primary_key=True)
    form_title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.form_title


class Feedback(models.Model):
    feedback_id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="feedback_entries")
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, related_name="feedback_entries")
    feedback_form = models.ForeignKey(FeedbackForm, on_delete=models.PROTECT, related_name="responses")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    teaching_clarity = models.PositiveSmallIntegerField(
        "Teaching clarity", validators=[MinValueValidator(1), MaxValueValidator(5)], default=5
    )
    communication = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=5
    )
    punctuality = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=5
    )
    feedback_message = models.TextField(blank=True)
    feedback_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-feedback_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["student", "faculty", "feedback_form"],
                name="one_response_per_student_faculty_form",
            )
        ]

    def __str__(self):
        return f"{self.student_id} → {self.faculty.faculty_name} ({self.rating}/5)"
