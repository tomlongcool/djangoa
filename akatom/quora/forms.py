from django.forms import ModelForm
from markdownx.fields import MarkdownxFormField


from akatom.quora.models import Question


class QuestionForm(ModelForm):
    content = MarkdownxFormField()

    class Meta:
        model = Question
        fields = ["title", "status", "content", "tags"]
