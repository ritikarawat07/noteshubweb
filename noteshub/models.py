from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager


# -------------------------
# Custom User Manager
# -------------------------
class UserManager(BaseUserManager):

    def create_user(self, roll_no, password=None, **extra_fields):
        if not roll_no:
            raise ValueError("Users must have a roll number")

        user = self.model(
            roll_no=roll_no,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, roll_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_teacher', True)
        extra_fields.setdefault('is_student', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(roll_no, password, **extra_fields)


# -------------------------
# Custom User Model
# -------------------------
class CustomUser(AbstractUser):

    # 🔴 REMOVE default username completely
    username = None

    roll_no = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    dob = models.DateField()

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'roll_no'
    REQUIRED_FIELDS = ['full_name', 'dob']

    objects = UserManager()

    def __str__(self):
        return self.roll_no or "User"


# -------------------------
# Notes Model
# -------------------------
class Notes(models.Model):

    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    year = models.CharField(max_length=10)
    branch = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)

    pdf = models.FileField(
        upload_to='noteshub/Notes_pdfs/',
        validators=[FileExtensionValidator(['pdf'])]
    )

    uploaded_at = models.DateTimeField(default=timezone.now)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.subject} - {self.chapter}"
