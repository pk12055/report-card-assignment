import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from accounts.managers import UserManager


class Student(AbstractUser):
    """
    This model stores the information of an Student.
    """
    username = None
    email = models.EmailField(unique=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    roll_number = models.CharField(unique=True, max_length=255)
    class_name = models.CharField(max_length=50, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)


    objects = UserManager()
    USERNAME_FIELD = 'roll_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.id)


class Subject(models.Model):
    """
    This model stores the subjects of students.
    """

    subject_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class StudentMark(models.Model):
    """
    This model stores the marks of students.
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_name')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_subject')
    marks = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return '{}'.format(self.subject.subject_name)


class ReportCardID(models.Model):
    """
    This model stores the id of report card.
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_report_id')
    report_id = models.CharField(null=True, blank=True, max_length=255)
    status = models.CharField(null=True, blank=True, max_length=255)
    task_id = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return '{}'.format(self.report_id)

