from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Student, StudentAccount, Faculty, FeedbackForm, Feedback


class CampusPulseRoleTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            uid="S001", class_name="FY B.Tech", subject="Information Technology"
        )
        self.faculty = Faculty.objects.create(
            faculty_id="F001", faculty_name="Dr. Demo Faculty"
        )
        self.feedback_form = FeedbackForm.objects.create(
            feedback_form_id="FF001", form_title="Teaching Feedback", is_active=True
        )

    def test_student_can_register_with_a_pre_registered_uid(self):
        response = self.client.post(reverse("student_register"), {
            "student_uid": "S001",
            "email": "student@example.edu",
            "password": "CampusPulse!2026Strong",
            "confirm_password": "CampusPulse!2026Strong",
        })
        self.assertRedirects(response, reverse("student_dashboard"))
        user = User.objects.get(username="S001")
        self.assertTrue(StudentAccount.objects.filter(user=user, student=self.student).exists())

    def test_student_cannot_open_admin_dashboard(self):
        user = User.objects.create_user(username="S001", password="StudentPass!23456")
        StudentAccount.objects.create(user=user, student=self.student)
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, reverse("student_dashboard"))

    def test_student_feedback_uses_the_logged_in_students_uid(self):
        user = User.objects.create_user(username="S001", password="StudentPass!23456")
        StudentAccount.objects.create(user=user, student=self.student)
        self.client.force_login(user)
        response = self.client.post(reverse("give_feedback"), {
            "faculty": "F001",
            "feedback_form": "FF001",
            "rating": "5",
            "teaching_clarity": "5",
            "communication": "4",
            "punctuality": "5",
            "feedback_message": "Very clear teaching.",
        })
        self.assertRedirects(response, reverse("thank_you"))
        feedback = Feedback.objects.get()
        self.assertEqual(feedback.student, self.student)
        self.assertEqual(feedback.rating, 5)

    def test_student_can_rate_any_faculty_and_each_feedback_criterion(self):
        another_faculty = Faculty.objects.create(
            faculty_id="F002", faculty_name="Prof. Example Faculty"
        )
        user = User.objects.create_user(
            username="S001", password="StrongPass!2026"
        )
        StudentAccount.objects.create(user=user, student=self.student)
        self.client.force_login(user)

        response = self.client.post(reverse("give_feedback"), {
            "faculty": another_faculty.faculty_id,
            "feedback_form": self.feedback_form.feedback_form_id,
            "rating": "4",
            "teaching_clarity": "3",
            "communication": "5",
            "punctuality": "4",
            "feedback_message": "Helpful and respectful feedback.",
        })

        self.assertRedirects(response, reverse("thank_you"))
        feedback = Feedback.objects.get()
        self.assertEqual(feedback.faculty, another_faculty)
        self.assertEqual(feedback.teaching_clarity, 3)
        self.assertEqual(feedback.communication, 5)
        self.assertEqual(feedback.punctuality, 4)

    def test_student_can_review_multiple_faculty_members_in_the_same_form(self):
        another_faculty = Faculty.objects.create(
            faculty_id="F002", faculty_name="Prof. Another Faculty"
        )
        user = User.objects.create_user(username="S001", password="StrongPass!2026")
        StudentAccount.objects.create(user=user, student=self.student)
        self.client.force_login(user)
        payload = {
            "feedback_form": self.feedback_form.feedback_form_id,
            "rating": "4",
            "teaching_clarity": "4",
            "communication": "4",
            "punctuality": "4",
            "feedback_message": "Helpful feedback.",
        }

        payload["faculty"] = self.faculty.faculty_id
        first_response = self.client.post(reverse("give_feedback"), payload)
        second_faculty_form = self.client.get(
            reverse("give_feedback"), {"faculty": another_faculty.faculty_id}
        )
        self.assertEqual(
            second_faculty_form.context["form"]["faculty"].value(),
            another_faculty.faculty_id,
        )

        payload["faculty"] = another_faculty.faculty_id
        second_response = self.client.post(reverse("give_feedback"), payload)

        self.assertRedirects(first_response, reverse("thank_you"))
        self.assertRedirects(second_response, reverse("thank_you"))
        self.assertSetEqual(
            set(Feedback.objects.values_list("faculty_id", flat=True)),
            {self.faculty.faculty_id, another_faculty.faculty_id},
        )

    def test_student_can_submit_only_once_per_faculty_and_form(self):
        user = User.objects.create_user(
            username="S001", password="StrongPass!2026"
        )
        StudentAccount.objects.create(user=user, student=self.student)
        self.client.force_login(user)
        payload = {
            "faculty": self.faculty.faculty_id,
            "feedback_form": self.feedback_form.feedback_form_id,
            "rating": "5",
            "teaching_clarity": "5",
            "communication": "5",
            "punctuality": "5",
            "feedback_message": "Excellent.",
        }

        first_response = self.client.post(reverse("give_feedback"), payload)
        duplicate_response = self.client.post(reverse("give_feedback"), payload)

        self.assertRedirects(first_response, reverse("thank_you"))
        self.assertEqual(duplicate_response.status_code, 200)
        self.assertContains(duplicate_response, "already submitted feedback")
        self.assertEqual(Feedback.objects.count(), 1)

        another_form = FeedbackForm.objects.create(
            feedback_form_id="FF002", form_title="Course Feedback", is_active=True
        )
        payload["feedback_form"] = another_form.feedback_form_id
        another_form_response = self.client.post(reverse("give_feedback"), payload)
        self.assertRedirects(another_form_response, reverse("thank_you"))
        self.assertEqual(Feedback.objects.count(), 2)

    def test_seed_demo_adds_repeatable_synthetic_responses(self):
        call_command("seed_demo", verbosity=0)
        call_command("seed_demo", verbosity=0)

        self.assertEqual(Feedback.objects.count(), 4)
        self.assertEqual(
            Feedback.objects.filter(student_id="SDEMO").count(),
            4,
        )

    def test_anonymous_user_cannot_open_student_dashboard(self):
        response = self.client.get(reverse("student_dashboard"))
        self.assertRedirects(response, f"{reverse('student_login')}?next={reverse('student_dashboard')}")

    def test_admin_staff_user_can_open_admin_dashboard(self):
        admin = User.objects.create_user(
            username="campusadmin", password="AdminPass!23456", is_staff=True
        )
        self.client.force_login(admin)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "STUDENT LOGINS")
