from django.core.management.base import BaseCommand
from feedback.models import Student, Faculty, FeedbackForm, Feedback


class Command(BaseCommand):
    help = "Create sample campus records and synthetic feedback for a quick demo."

    def handle(self, *args, **options):
        # These sample IDs and details follow the schema reference image in this project.
        students = [
            ("S001", "FY B.Tech", "Chemical Engineering"),
            ("S002", "FY B.Tech", "Information Technology"),
            ("S003", "SY B.Tech", "Chemical Engineering"),
            ("SDEMO", "Demo data", "Synthetic examples only"),
        ]
        for uid, class_name, subject in students:
            Student.objects.get_or_create(
                uid=uid, defaults={"class_name": class_name, "subject": subject}
            )

        faculty = [
            ("F001", "Dr. S. Kumar", "9876500001", "s.kumar@example.edu", "022-000001", "Nanded"),
            ("F002", "Prof. A. Sharma", "8765400002", "a.sharma@example.edu", "022-000002", "Pune"),
            ("F003", "Dr. V. Patil", "7654300003", "v.patil@example.edu", "022-000003", "Mumbai"),
        ]
        for faculty_id, name, mobile, email, phone, address in faculty:
            Faculty.objects.get_or_create(
                faculty_id=faculty_id,
                defaults={
                    "faculty_name": name,
                    "mobile_no": mobile,
                    "email_id": email,
                    "phone": phone,
                    "address": address,
                },
            )

        forms = [
            ("FF001", "Faculty Teaching Feedback", "Share your experience of the faculty's teaching."),
            ("FF002", "Course & Learning Feedback", "Help us improve the course and learning experience."),
        ]
        for form_id, title, description in forms:
            FeedbackForm.objects.get_or_create(
                feedback_form_id=form_id,
                defaults={"form_title": title, "description": description, "is_active": True},
            )

        sample_feedback = [
            ("SDEMO", "F001", "FF001", 5, 5, 4, 5, "Clear explanations and helpful examples."),
            ("SDEMO", "F002", "FF001", 4, 4, 5, 4, "Encourages questions and communicates clearly."),
            ("SDEMO", "F003", "FF001", 4, 5, 4, 3, "The sessions are useful; sharing notes earlier would help."),
            ("SDEMO", "F001", "FF002", 4, 4, 5, 5, "A positive learning experience overall."),
        ]
        for uid, faculty_id, form_id, rating, clarity, communication, punctuality, comment in sample_feedback:
            Feedback.objects.get_or_create(
                student_id=uid,
                faculty_id=faculty_id,
                feedback_form_id=form_id,
                defaults={
                    "rating": rating,
                    "teaching_clarity": clarity,
                    "communication": communication,
                    "punctuality": punctuality,
                    "feedback_message": comment,
                },
            )

        self.stdout.write(self.style.SUCCESS(
            "Demo records are ready. Register a student account for S001, S002, or S003 at /student/register/ "
            "to submit feedback. Sample ratings are stored under the SDEMO synthetic student."
        ))
