from datetime import datetime

from django.shortcuts import render
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_412_PRECONDITION_FAILED, HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST
# Create your views here.


from .models import Question, Tenant, APIHitsLog, QaUser


def get_question_answers(question):
    """ get a dictionary of question answers for a given instance of Question"""

    return dict(title=question.title,
         question_id=question.id,
         user_id=question.user_id,
         user_name=question.user.name,
         answers=[
             {'answer_id': answer.id, 'answer': answer.body, 'user_name': answer.user.name,
              'user_id': answer.user_id} for
             answer in question.answer_set.all()
         ]
         )


class Questionnaire(APIView):
    """
    read-only API to allow consumers to retrieve Questions with Answers as JSON.
    The response includes Answers inside their
    Question as well as include the id and name of the Question and Answer users.
    """
    throttle_scope = 'burst'
    no_such_tenant = False
    REQ_PER_DAY_THRESHOLD = 1

    def get_throttles(self):
        api_key = self.kwargs['key']
        try:
            tenant = Tenant.objects.get(api_key=api_key)
            api_hits_log, _ = APIHitsLog.objects.get_or_create(tenant=tenant, path=self.request.META.get('PATH_INFO'),
                                                            day=datetime.now().date())
            api_hits_log.hits += 1
            api_hits_log.save()
            if api_hits_log.hits > self.REQ_PER_DAY_THRESHOLD:
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
            result.append(get_question_answers(question))
        return Response({
            'status_code': HTTP_200_OK,
            'message': '',
            'result': result
        })


class Dashboard(View):
    """ Add an HTML dashboard page as the root URL that shows the total number of Users, Questions, and Answers in the
    system, as well as Tenant API request counts for all Tenants."""
    template_name = 'dashboard.html'

    def get(self, request):
        user_count = QaUser.objects.count()
        questions = Question.objects.all()
        qna = [get_question_answers(question) for question in questions]
        tenant_api_counts = [{'name': api_log.tenant.name,
                              'day': api_log.day,
                              'count': api_log.hits} for api_log in APIHitsLog.objects.all()
                             ]
        context = dict(user_count = user_count, qna=qna, tenant_api_counts=tenant_api_counts)
        return render(request, self.template_name, context)
