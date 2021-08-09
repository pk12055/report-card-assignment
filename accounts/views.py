import os
import base64

from rest_framework import generics
from rest_framework.response import Response
from accounts.utils import Mailer

from accounts.models import Student, Subject, StudentMark, ReportCardID
from accounts.serializers import (
    StudentSerializer, SubjectSerializer, StudentMarkSerializer,
    ReportCardSerializer, CardIdStatusSerializer
)
from student.celery import send_report_card_email
from celery.result import AsyncResult


class StudentCreateApi(generics.CreateAPIView):
    # API to add new student with the essential data

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentListApi(generics.ListAPIView):
    # API to get list of already added student

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentUpdateApi(generics.RetrieveUpdateAPIView):
    # API to update the already added student with the essential data

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDeleteApi(generics.DestroyAPIView):
    # API to delete the already added student with the essential data

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class SubjectCreateApi(generics.CreateAPIView):
    # API to add the subject of student

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectListApi(generics.ListAPIView):
    # API to get list of all the subject of student

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectUpdateApi(generics.RetrieveUpdateAPIView):
    # API to update the subject of student

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDeleteApi(generics.DestroyAPIView):
    # API to delete the subject of student

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class StudentMarkCreateApi(generics.CreateAPIView):
    # API to add the marks of student for a particular subject

    queryset = StudentMark.objects.all()
    serializer_class = StudentMarkSerializer

    def post(self, request, format=None):
        serializer = StudentMarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.validated_data["student"]
        subject = serializer.validated_data["subject"]
        marks = serializer.validated_data["marks"]

        if StudentMark.objects.filter(student=student, subject=subject).exists():
            mark = StudentMark.objects.get(student=student, subject=subject)
            mark.marks = marks
            mark.save()

        else:
            StudentMark.objects.create(
                student=student, subject=subject, marks=marks)

        response = {
            "student": student.roll_number,
            "subject": subject.subject_name,
            "marks": marks
        }
        return Response(response)


class StudentMarkListApi(generics.ListAPIView):
    # API to get the list of marks of student of all subject

    queryset = StudentMark.objects.all()
    serializer_class = StudentMarkSerializer


class StudentMarkUpdateApi(generics.RetrieveUpdateAPIView):
    # API to update the marks of student of a subject

    queryset = StudentMark.objects.all()
    serializer_class = StudentMarkSerializer


class StudentMarkDeleteApi(generics.DestroyAPIView):
    # API to delete marks of student of a subject

    queryset = StudentMark.objects.all()
    serializer_class = StudentMarkSerializer


class ReportCardCreateApi(generics.CreateAPIView):
    # API to get the report card of student on mail and generate id to track the status

    serializer_class = ReportCardSerializer

    def post(self, request, format=None):
        serializer = ReportCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        roll_number = serializer.validated_data["roll_number"]

        student = Student.objects.get(roll_number=roll_number)
        marks = StudentMark.objects.filter(student=student)

        mark_list = []
        for mark in marks:
            mark_list.append(mark.marks)

        total_marks = 0
        for i in range(0, len(mark_list)):
            total_marks = total_marks + mark_list[i]

        report_id = base64.b64encode(os.urandom(6)).decode('ascii')

        task = send_report_card_email.delay(student.id, total_marks, report_id)

        report_card_id = ReportCardID.objects.create(
            report_id=report_id, student=student, status='PENDING', task_id=task.task_id)

        response = {
            "response": 'Your report card will be mailed to you shortly',
            "ReportCard Tracking id": report_id
        }
        return Response(response)


class CardIdStatusCreateApi(generics.CreateAPIView):
    # API to check the status of report card email with the help of tracking id

    serializer_class = CardIdStatusSerializer

    def post(self, request, format=None):
        serializer = CardIdStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report_id = serializer.validated_data["report_id"]
        status = ReportCardID.objects.get(report_id=report_id)

        response = {
            'status': status.status,
            "ReportCard Tracking id": report_id
        }
        return Response(response)
