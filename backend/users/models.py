from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

class User(AbstractUser):
    """
    Custom user model.
    - Uses email as the unique identifier.
    - Adds role, full_name, and other profile fields.
    - Inherits fields like password, last_login, is_superuser from AbstractUser.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        NURSE = "nurse", "Nurse"
        DOCTOR = "doctor", "Doctor"
        PATIENT = "patient", "Patient"

    # AbstractUser has a 'username' field. We set it to None to indicate
    # we are not using it, in favor of 'email'.
    username = None
    email = models.EmailField("email address", unique=True)

    # Custom fields
    role = models.CharField(max_length=10, choices=Role.choices)
    full_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)  # `date_joined` from AbstractUser serves as `created_at`

    USERNAME_FIELD = "email"
    # 'email' and 'password' are required by default.
    # These fields will be prompted for when using the `createsuperuser` command.
    REQUIRED_FIELDS = ["full_name", "role"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email


class GeneralDoctorProfile(models.Model):
    """Profile model for users with the 'doctor' role."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile")
    license_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True)
    available_for_consultation = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "general_doctor_profiles"
        verbose_name = "General Doctor Profile"
        verbose_name_plural = "General Doctor Profiles"

    def __str__(self):
        return f"Dr. {self.user.full_name} - {self.specialization}"


class NurseProfile(models.Model):
    """Profile model for users with the 'nurse' role."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="nurse_profile")
    license_number = models.CharField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        db_table = "nurse_profiles"
        verbose_name = "Nurse Profile"
        verbose_name_plural = "Nurse Profiles"

    def __str__(self):
        return f"Nurse {self.user.full_name}"
    
    #patient profile
class PatientProfile(models.Model):
    """Profile model for users with the 'patient' role."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile")
    

    # Note: Name, Age, and Gender are sourced from the related User model.
    # Age can be calculated from user.date_of_birth.

    class BloodType(models.TextChoices):
        A_POSITIVE = "A+", "A+"
        A_NEGATIVE = "A-", "A-"
        B_POSITIVE = "B+", "B+"
        B_NEGATIVE = "B-", "B-"
        AB_POSITIVE = "AB+", "AB+"
        AB_NEGATIVE = "AB-", "AB-"
        O_POSITIVE = "O+", "O+"
        O_NEGATIVE = "O-", "O-"
        UNKNOWN = "UNK", "Unknown"

    blood_type = models.CharField(
        max_length=3, choices=BloodType.choices, default=BloodType.UNKNOWN, blank=True
    )
    medical_condition = models.TextField(
        blank=True, help_text="A summary of the patient's current medical condition."
    )
    date_of_admission = models.DateField(null=True, blank=True)
    discharge_date = models.DateField(null=True, blank=True)
    assigned_doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients",
        limit_choices_to={"role": User.Role.DOCTOR},
        help_text="The primary doctor assigned to this patient.",
    )
    medication = models.TextField(blank=True, help_text="List of prescribed medications.")
    test_results = models.TextField(blank=True, help_text="Summary of recent test results.")

    class Meta:
        db_table = "patient_profiles"
        verbose_name = "Patient Profile"
        verbose_name_plural = "Patient Profiles"

    def __str__(self):
        return f"Patient {self.user.full_name}"