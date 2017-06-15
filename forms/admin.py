from django.contrib import admin

from .models import Form, Question, Choice, TextAnswer, McqOneAnswer, \
                    McqManyAnswer, BinaryAnswer
                    

class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'form')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice_text', 'question')


class TextAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'user')


class McqOneAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice', 'question', 'user')


class McqManyAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_choices', 'question', 'user')


class BinaryAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer_option', 'question', 'user')


admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(TextAnswer, TextAnswerAdmin)
admin.site.register(McqOneAnswer, McqOneAnswerAdmin)
admin.site.register(McqManyAnswer, McqManyAnswerAdmin)
admin.site.register(BinaryAnswer, BinaryAnswerAdmin)