from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Faculty",
            fields=[
                ("faculty_id", models.CharField(max_length=30, primary_key=True, serialize=False)),
                ("faculty_name", models.CharField(max_length=120)),
                ("mobile_no", models.CharField(blank=True, max_length=15)),
                ("email_id", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("address", models.TextField(blank=True)),
            ],
            options={"ordering": ["faculty_name"], "verbose_name_plural": "Faculty"},
        ),
        migrations.CreateModel(
            name="FeedbackForm",
            fields=[
                ("feedback_form_id", models.CharField(max_length=30, primary_key=True, serialize=False)),
                ("form_title", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("uid", models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name="School UID")),
                ("class_name", models.CharField(max_length=40, verbose_name="Class / Standard")),
                ("subject", models.CharField(max_length=100)),
            ],
            options={"ordering": ["uid"]},
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("feedback_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("rating", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("teaching_clarity", models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name="Teaching clarity")),
                ("communication", models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("punctuality", models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("feedback_message", models.TextField(blank=True)),
                ("feedback_date", models.DateTimeField(auto_now_add=True)),
                ("faculty", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="feedback_entries", to="feedback.faculty")),
                ("feedback_form", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="responses", to="feedback.feedbackform")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="feedback_entries", to="feedback.student")),
            ],
            options={"ordering": ["-feedback_date"]},
        ),
        migrations.AddConstraint(
            model_name="feedback",
            constraint=models.UniqueConstraint(fields=("student", "faculty", "feedback_form"), name="one_response_per_student_faculty_form"),
        ),
    ]
