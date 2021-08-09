from django.conf import settings as conf_settings
from rest_framework import serializers
import re

from accounts.models import Student, Subject, StudentMark, ReportCardID

class StudentSerializer(serializers.ModelSerializer):
    # serializer class to validate the student requird data

    class Meta:
        model = Student
        exclude = ['password',]


    def validate(self, data):
        # validate if student added is having class, first name, roll number and father name

        roll_number = data.get("roll_number", "")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        mother_name = data.get("mother_name", "")
        father_name = data.get("father_name", "")
        class_name = data.get("class_name", "")

        if not class_name:
            raise serializers.ValidationError("Please provide Class")

        if not first_name:
            raise serializers.ValidationError("Please provide First Name")

        if not father_name:
            raise serializers.ValidationError("Please provide Father Name")

        string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        # checks the name's with regex string of special characters, if exists than raise errors
        if(string_check.search(first_name)):
            raise serializers.ValidationError("First Name can not contain special character")

        if(string_check.search(last_name)):
            raise serializers.ValidationError("Last Name can not contain special character")

        if(string_check.search(father_name)):
            raise serializers.ValidationError("Father Name can not contain special character")

        if(string_check.search(mother_name)):
            raise serializers.ValidationError("Mother Name can not contain special character")


        if not roll_number:
            raise serializers.ValidationError(
                "Please enter roll number of Student"
            )

        if (Student.objects.filter(roll_number=roll_number).exists()):
            raise serializers.ValidationError(
                "Student with same roll number already exists!"
            )

        return data


class SubjectSerializer(serializers.ModelSerializer):
    # serializer class to validate the student subject

    class Meta:
        model = Subject
        exclude = []

    def validate(self, data):
        # validate if subject is there or not

        subject_name = data.get("subject_name", "")

        if not subject_name:
            raise serializers.ValidationError(
                "Please enter Subject"
            )

        if Subject.objects.filter(subject_name=subject_name).exists():
            raise serializers.ValidationError(
                "Subject already exists"
            )

        return data


class StudentMarkSerializer(serializers.ModelSerializer):
    # serializer class to validate the student marks of a particular subject

    class Meta:
        model = StudentMark
        exclude = []

    def validate(self, data):
        marks = data.get("marks", "")

        if not marks:
            raise serializers.ValidationError(
                "Please enter Marks"
            )

        if marks < 0:
            raise serializers.ValidationError(
                "Please enter Marks in positive number"
            )

        return data


class ReportCardSerializer(serializers.Serializer):
    # serializer class to validate the roll number and student to get the report card of email

    roll_number = serializers.IntegerField(write_only=True)

    def validate(self, data):
        roll_number = data.get("roll_number", "")

        if not roll_number:
            raise serializers.ValidationError(
                "Please enter Roll Number"
            )

        if roll_number < 0:
            raise serializers.ValidationError(
                "Please enter valid Roll Number"
            )

        if not Student.objects.filter(roll_number=roll_number).exists():
            raise serializers.ValidationError(
                "Student with this Roll Number not exists"
            )

        if not StudentMark.objects.filter(student=Student.objects.get(roll_number=roll_number)).exists():
            raise serializers.ValidationError(
                "Marks are not yet updated for this student"
            )

        return data


class CardIdStatusSerializer(serializers.Serializer):
    # serializer class to get the tracking status of email

    report_id = serializers.CharField(write_only=True)

    def validate(self, data):
        report_id = data.get("report_id", "")

        if not report_id:
            raise serializers.ValidationError(
                "Please enter Report Tracking Id"
            )

        if not ReportCardID.objects.filter(report_id=report_id).exists():
            raise serializers.ValidationError(
                "Tracking Id does not exist"
            )

        return data
