from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_412_PRECONDITION_FAILED, HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST
# Create your views here.


# Add a RESTful, read-only API to allow consumers to retrieve Questions with Answers as JSON
# (no need to retrieve Answers on their own). The response should include Answers inside their
# Question as well as include the id and name of the Question and Answer users.
from .models import Question, Tenant, APIHitsLog


class Questionnaire(APIView):
    """
    read-only API to allow consumers to retrieve Questions with Answers as JSON.
    The response includes Answers inside their
    Question as well as include the id and name of the Question and Answer users.
    """
    throttle_scope = 'burst'
    no_such_tenant = False
    REQ_PER_DAY_THRESHOLD = 100

    def get_throttles(self):
        api_key = self.kwargs['key']
        try:
            tenant = Tenant.objects.get(api_key=api_key)
            api_hits_log, _ = APIHitsLog.objects.get_or_create(tenant=tenant, path=self.request.META.get('PATH_INFO'),
                                                            day=datetime.now().date())
            api_hits_log.hits_today += 1
            api_hits_log.save()
            if api_hits_log.hits_today > self.REQ_PER_DAY_THRESHOLD:
                self.throttle_scope = 'sustained'
        except Tenant.DoesNotExist:
            self.no_such_tenant = True
        return super(Questionnaire, self).get_throttles()

    def get(self, request, key):
        """
        Return JSON response containing question(s) based on search criteria and their answers
        :param request: HTTP request object
        :return: JSON
        """
        if self.no_such_tenant:
            return Response({
                'status_code': HTTP_400_BAD_REQUEST,
                'message': 'Invalid api key %s' % key
            })
        search_text = request.GET.get("search")
        question_id = request.GET.get("q")
        result = list()

        # validate if either of the parameters is set
        if not search_text and not question_id:
            return Response({
                'status_code': HTTP_412_PRECONDITION_FAILED,
                'message': 'Invalid or No parameters received',
                'result': result
            })

        if search_text:
            questions = Question.objects.filter(title__icontains=search_text, private=False) if search_text else None
        elif question_id:
            questions = Question.objects.filter(id=question_id, private=False)

        if not questions:
            return Response({
                'status_code': HTTP_204_NO_CONTENT,
                'message': 'No questions found',
                'result': result
            })

        # prepare the answer json for the matching set of questions
        for question in questions:
            result.append(dict(title=question.title,
                               question_id=question.id,
                               user_id=question.user_id.id,
                               user_name=question.user_id.name,
                               answers=[
                                   {'answer_id': answer.id, 'answer': answer.body, 'user_name': answer.user_id.name,
                                    'user_id': answer.user_id.id} for
                                   answer in question.answer_set.all()
                               ]
                               ))
        return Response({
            'status_code': HTTP_200_OK,
            'message': '',
            'result': result
        })
