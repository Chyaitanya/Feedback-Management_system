from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Avg, Count
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import AdminLoginForm, FeedbackSubmissionForm, StudentLoginForm, StudentSignupForm
from .models import Student, StudentAccount, Faculty, Feedback, FeedbackForm


def _send_user_to_home(user):
    if user.is_staff:
        return "dashboard"
    if StudentAccount.objects.filter(user=user).exists():
        return "student_dashboard"
    return "portal"


def portal(request):
    if request.user.is_authenticated:
        destination = _send_user_to_home(request.user)
        if destination != "portal":
            return redirect(destination)
    return render(request, "feedback/portal.html")


def student_login(request):
    if request.user.is_authenticated:
        return redirect(_send_user_to_home(request.user))
    form = StudentLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["student_uid"].strip(),
            password=form.cleaned_data["password"],
        )
        if user is not None and StudentAccount.objects.filter(user=user).exists():
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! Your student space is ready.")
            return redirect("student_dashboard")
        form.add_error(None, "Student login details are incorrect, or this account is not a student account.")
    return render(request, "feedback/student_login.html", {"form": form})


def admin_login(request):
    if request.user.is_authenticated:
        return redirect(_send_user_to_home(request.user))
    form = AdminLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"].strip(),
            password=form.cleaned_data["password"],
        )
        if user is not None and user.is_active and user.is_staff:
            login(request, user)
            messages.success(request, "Admin access granted. Welcome to the control room!")
            return redirect("dashboard")
        form.add_error(None, "Admin login failed. Use an active staff/admin account.")
    return render(request, "feedback/admin_login.html", {"form": form})


def student_register(request):
    if request.user.is_authenticated:
        return redirect(_send_user_to_home(request.user))
    form = StudentSignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.create_account()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, "Your student account is ready. Welcome to Overall Feedback System!")
        return redirect("student_dashboard")
    return render(request, "feedback/student_register.html", {"form": form})


@require_POST
@login_required(login_url="portal")
def logout_view(request):
    logout(request)
    messages.success(request, "You have been signed out safely.")
    return redirect("portal")


def admin_required(view_func):
    @login_required(login_url="admin_login")
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "This area is only available to admin users.")
            return redirect("student_dashboard") if StudentAccount.objects.filter(user=request.user).exists() else redirect("portal")
        return view_func(request, *args, **kwargs)
    return wrapped


def student_required(view_func):
    @login_required(login_url="student_login")
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not StudentAccount.objects.filter(user=request.user).exists():
            messages.error(request, "Please sign in with a student account to continue.")
            return redirect("dashboard") if request.user.is_staff else redirect("portal")
        return view_func(request, *args, **kwargs)
    return wrapped


@admin_required
def dashboard(request):
    stats = {
        "students": Student.objects.count(),
        "accounts": StudentAccount.objects.count(),
        "faculty": Faculty.objects.count(),
        "responses": Feedback.objects.count(),
        "average": Feedback.objects.aggregate(value=Avg("rating"))["value"],
        "forms": FeedbackForm.objects.filter(is_active=True).count(),
    }
    recent = Feedback.objects.select_related("student", "faculty", "feedback_form")[:6]
    top_faculty = Faculty.objects.annotate(
        response_count=Count("feedback_entries"),
        avg_rating=Avg("feedback_entries__rating")
    ).order_by("-avg_rating")[:5]
    return render(request, "feedback/dashboard.html", {
        "stats": stats, "recent": recent, "top_faculty": top_faculty
    })


@student_required
def student_dashboard(request):
    student = request.user.student_account.student
    own_feedback = Feedback.objects.filter(student=student).select_related("faculty", "feedback_form")
    context = {
        "student": student,
        "own_feedback": own_feedback[:8],
        "feedback_count": own_feedback.count(),
        "active_forms": FeedbackForm.objects.filter(is_active=True).count(),
        "faculty_count": Faculty.objects.count(),
        "faculty_members": Faculty.objects.all(),
    }
    return render(request, "feedback/student_dashboard.html", context)


@student_required
def give_feedback(request):
    student = request.user.student_account.student
    if request.method == "POST":
        form = FeedbackSubmissionForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.student = student
            try:
                with transaction.atomic():
                    entry.save()
                messages.success(request, "Your feedback has been submitted. Thank you!")
                return redirect("thank_you")
            except IntegrityError:
                form.add_error(None, "You have already submitted feedback for this faculty member and form.")
    else:
        selected_faculty = Faculty.objects.filter(pk=request.GET.get("faculty")).first()
        form = FeedbackSubmissionForm(initial={"faculty": selected_faculty} if selected_faculty else None)
    return render(request, "feedback/give_feedback.html", {"form": form, "student": student})


@student_required
def thank_you(request):
    return render(request, "feedback/thank_you.html")


@admin_required
def faculty_list(request):
    faculty = Faculty.objects.annotate(
        response_count=Count("feedback_entries"),
        avg_rating=Avg("feedback_entries__rating")
    )
    return render(request, "feedback/faculty.html", {"faculty": faculty})


@admin_required
def feedback_list(request):
    responses = Feedback.objects.select_related("student", "faculty", "feedback_form")
    return render(request, "feedback/responses.html", {"responses": responses})
