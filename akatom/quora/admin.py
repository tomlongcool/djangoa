from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from akatom.quora.models import Vote, Question, Answer


class VoteAdmin(admin.ModelAdmin):
    list_display = ["uuid_id", "user", "value", "content_type", "object_id", "vote"]


class QuestionAdmin(MarkdownxModelAdmin):
    list_display = ['id', "user", "title", "slug", "status", "tags", "has_correct"]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['uuid', "user", "question", "is_accepted"]


admin.site.register(Vote, VoteAdmin)
admin.site.register(Question, MarkdownxModelAdmin)
admin.site.register(Answer, AnswerAdmin)
