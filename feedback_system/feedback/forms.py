from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Feedback, Student, StudentAccount, Faculty, FeedbackForm


class StudentSignupForm(forms.Form):
    student_uid = forms.CharField(
        label="Student UID", max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. STU001", "autocomplete": "username"}),
    )
    email = forms.EmailField(
        label="College email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@college.edu", "autocomplete": "email"}),
    )
    password = forms.CharField(
        label="Create password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "At least 8 characters", "autocomplete": "new-password"}),
    )
    confirm_password = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password again", "autocomplete": "new-password"}),
    )

    def clean_student_uid(self):
        uid = self.cleaned_data["student_uid"].strip()
        try:
            student = Student.objects.get(uid__iexact=uid)
        except Student.DoesNotExist:
            raise ValidationError("This Student UID is not registered yet. Ask your admin to add your student record.")
        if StudentAccount.objects.filter(student=student).exists():
            raise ValidationError("An account already exists for this Student UID. Please sign in instead.")
        if User.objects.filter(username__iexact=student.uid).exists():
            raise ValidationError("This Student UID is already in use. Please contact the admin.")
        return student.uid

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already linked to an account.")
        return email

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirm_password = cleaned.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "The passwords do not match.")
        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                self.add_error("password", error)
        return cleaned

    @transaction.atomic
    def create_account(self):
        student = Student.objects.get(uid=self.cleaned_data["student_uid"])
        user = User.objects.create_user(
            username=student.uid,
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        StudentAccount.objects.create(user=user, student=student)
        return user


class StudentLoginForm(forms.Form):
    student_uid = forms.CharField(
        label="Student UID", max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your Student UID", "autocomplete": "username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password", "autocomplete": "current-password"}),
    )


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        label="Admin username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter admin username", "autocomplete": "username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter admin password", "autocomplete": "current-password"}),
    )


class FeedbackSubmissionForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            "faculty", "feedback_form", "rating",
            "teaching_clarity", "communication", "punctuality", "feedback_message",
        ]
        widgets = {
            "faculty": forms.Select(attrs={"class": "form-control"}),
            "feedback_form": forms.Select(attrs={"class": "form-control"}),
            "rating": forms.Select(choices=[(i, f"{i} / 5") for i in range(1, 6)], attrs={"class": "form-control"}),
            "teaching_clarity": forms.Select(choices=[(i, f"{i} / 5") for i in range(1, 6)], attrs={"class": "form-control"}),
            "communication": forms.Select(choices=[(i, f"{i} / 5") for i in range(1, 6)], attrs={"class": "form-control"}),
            "punctuality": forms.Select(choices=[(i, f"{i} / 5") for i in range(1, 6)], attrs={"class": "form-control"}),
            "feedback_message": forms.Textarea(attrs={
                "class": "form-control", "rows": 4,
                "placeholder": "Share a helpful, respectful suggestion..."
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["faculty"].queryset = Faculty.objects.all()
        self.fields["feedback_form"].queryset = FeedbackForm.objects.filter(is_active=True)
        self.fields["faculty"].empty_label = "Choose a faculty member"
        self.fields["feedback_form"].empty_label = "Choose a feedback form"
