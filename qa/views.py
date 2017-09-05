from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_412_PRECONDITION_FAILED, HTTP_204_NO_CONTENT, HTTP_200_OK
# Create your views here.


#Add a RESTful, read-only API to allow consumers to retrieve Questions with Answers as JSON
# (no need to retrieve Answers on their own). The response should include Answers inside their
# Question as well as include the id and name of the Question and Answer users.
from .models import Question


class Questionnaire(APIView):
    def get(self, request):
        """
        Return JSON response containing question(s) based on search criteria and their answers
        :param request: HTTP request object
        :return: JSON
        """
        search_text = request.GET.get("search")
        question_id = request.GET.get("q")
        result = dict()

        # validate if either of the parameters is set
        if not search_text and not question_id:
            return Response({
                'status_code': HTTP_412_PRECONDITION_FAILED,
                'message': 'Invalid or No parameters received',
                'result': result
            })

        if search_text:
            questions = Question.objects.filter(title__icontains = search_text, private=False) if search_text else None
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
            q_id = question.id
            result[q_id] = dict(title=question.title,
                                answers=[
                                    {'answer_id': answer.id, 'answer': answer.body, 'user': answer.user_id.name} for
                                    answer in question.answer_set.all()
                                    ]
                                )
        return Response({
            'status_code': HTTP_200_OK,
            'message': '',
            'result': result
        })
