from django.urls import path
from . import views

urlpatterns = [
    path("", views.portal, name="portal"),
    path("student/login/", views.student_login, name="student_login"),
    path("student/register/", views.student_register, name="student_register"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("admin-login/", views.admin_login, name="admin_login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("give-feedback/", views.give_feedback, name="give_feedback"),
    path("thanks/", views.thank_you, name="thank_you"),
    path("faculty/", views.faculty_list, name="faculty_list"),
    path("responses/", views.feedback_list, name="feedback_list"),
]
