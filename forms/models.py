from django.db import models
from django.contrib.auth.models import User


class Form(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, default='1')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    form = models.ForeignKey(Form)
    QUESTION_TYPE_CHOICES = (
        ('text', 'Text based answer'),
        ('mcq_one', 'MCQ with single possible answer'),
        ('mcq_many', 'MCQ with multiple possible answers'),
        ('binary', 'Yes/No based answer')
    )
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='text')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TextAnswer(Answer):
    answer_text = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.id)


class McqOneAnswer(Answer):
    choice = models.ForeignKey(Choice)

    def __str__(self):
        return self.choice.choice_text


class McqManyAnswer(Answer):
    choices = models.ManyToManyField(Choice)

    def get_choices(self):
        return ",".join([str(choice) for choice in self.choices.all()])

    def __str__(self):
        return str(self.id)


class BinaryAnswer(Answer):
    ANSWER_OPTIONS = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    answer_option = models.CharField(max_length=3, choices=ANSWER_OPTIONS)

    def __str__(self):
        return self.answer_option