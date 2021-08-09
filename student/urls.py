from django.conf import settings
from django.conf.urls import url
from django.contrib import admin

from accounts.views import (
    StudentCreateApi, StudentListApi, StudentUpdateApi, StudentDeleteApi,
    SubjectCreateApi, SubjectListApi, SubjectUpdateApi, SubjectDeleteApi,
    StudentMarkCreateApi, StudentMarkListApi, StudentMarkUpdateApi, StudentMarkDeleteApi,
    ReportCardCreateApi, CardIdStatusCreateApi
    )

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"add/student/", StudentCreateApi.as_view()),
    url(r"list/student/", StudentListApi.as_view()),
    url(r"update/student/(?P<pk>\d+)/", StudentUpdateApi.as_view()),
    url(r"delete/student/(?P<pk>\d+)/", StudentDeleteApi.as_view()),
    url(r"add/subject/", SubjectCreateApi.as_view()),
    url(r"list/subject/", SubjectListApi.as_view()),
    url(r"update/subject/(?P<pk>\d+)/", SubjectUpdateApi.as_view()),
    url(r"delete/subject/(?P<pk>\d+)/", SubjectDeleteApi.as_view()),
    url(r"add/marks/", StudentMarkCreateApi.as_view()),
    url(r"list/marks/", StudentMarkListApi.as_view()),
    url(r"update/marks/(?P<pk>\d+)/", StudentMarkUpdateApi.as_view()),
    url(r"delete/marks/(?P<pk>\d+)/", StudentMarkDeleteApi.as_view()),
    url(r"generate/report/card/", ReportCardCreateApi.as_view()),
    url(r"get/card/id/status/", CardIdStatusCreateApi.as_view()),
]
