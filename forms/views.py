from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json

from .models import Form, Question, Choice
from .serializers import UserSerializer, FormSerializer, QuestionSerializer


class FormListView(LoginRequiredMixin, ListView):
    model = Form

    def get_queryset(self):
        return Form.objects.filter()


class FormCreate(LoginRequiredMixin, CreateView):
    model = Form
    template_name = 'forms/form_create.html'
    fields = '__all__'

    def post(self, request):
        result = {"result": "", "error_reason": ""}
        unicode_body = request.body.decode('utf-8')
        dict_post_data = json.loads(unicode_body)
        if len(dict_post_data['questions']) > 0:
            form = Form(title=dict_post_data['form_title'],
                        description=dict_post_data['form_description'],
                        owner=self.request.user)
            form.save()
            result['result'] = 'Form saved successfully'
            for question_item in dict_post_data['questions']:
                question = Question(question_text=question_item['text'],
                                    question_type=question_item['type'],
                                    form=form)
                question.save()
                if question_item['type'] == 'mcq_one' or question_item['type'] == 'mcq_many':
                    for choice_item in question_item['options']:
                        choice = Choice(choice_text=choice_item,
                                        question=question)
                        choice.save()
        else:
            result['result'] = 'Add a question title'
        return HttpResponse(json.dumps(result))


@login_required
def view_form(request, username, pk):
    user = User.objects.get(username=username)
    form = Form.objects.get(id=pk, owner=user)
    questions = Question.objects.filter(form=form)
    choices = Choice.objects.filter(question__in=questions)
    context = {
        'form': form,
        'questions': questions,
        'choices': choices
    }
    return render(request, 'forms/view_form.html', context)
    

# unused in app
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer