from django.contrib import admin
from .models import Profile, Question, Answer, Tag, QuestionLike, QuestionDislike, AnswerLike

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(QuestionLike)
admin.site.register(QuestionDislike)
admin.site.register(AnswerLike)
