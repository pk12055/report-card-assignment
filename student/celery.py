import os
import time

from celery import Celery
from django.apps import apps
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student.settings')

app = Celery('student')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



@app.task
def send_report_card_email(student, total_marks, report_id):
    time.sleep(10)

    # celery task to send email with the report card details of the student
    # also it updates the status of that tracking id

    from django.core.mail import send_mail
    from accounts.models import Student, ReportCardID

    student = Student.objects.get(id=student)
    report_id = ReportCardID.objects.get(report_id=report_id)

    report_id.status = 'RUNNING'
    report_id.save()
    try:
        subject = 'Report Card of {}'.format(student.first_name)
        message = f"""Please find the attached report of Student:
                        Name  : {student.first_name},
                        class : {student.class_name},
                        Father's name : {student.father_name},
                        Mother's name : {student.mother_name},
                        Total Marks obtain : {total_marks},
                    """
        recipient = [student.email]
        email_from = 'kumarpulkit35@gmail.com'
        send_mail(subject, message, email_from, recipient)
        report_id.status = 'SUCCESS'
        report_id.save()
    except Exception as e:
        report_id.status = 'FAIL'
        report_id.save()

