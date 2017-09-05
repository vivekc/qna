from django.core.urlresolvers import reverse
from rest_framework import status
from django.test import TestCase, Client

client = Client()


class QuestionnaireTest(TestCase):
    """ Test module for searching questions """

    def test_get_invalid_params(self):
        url = str(reverse('get_qna'))
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

