from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^api/v1/qna/',
        views.Questionnaire.as_view(),
        name='get_qna'
    ),
]