from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, DetailView

from akatom.autils import ajax_required
from akatom.quora.forms import QuestionForm
from akatom.quora.models import Question, Answer


class QuestionListView(ListView):
    """所有问题页"""
    model = Question
    paginate_by = 10
    context_object_name = "question_list"
    template_name = "quora/question-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context["popular_tags"] = Question.objects.get_counted_tags()  # 页面的标签功能
        context["active"] = "all"
        return context


class CorrectAnsweredQuestionListView(QuestionListView):
    """已有正确答案的问题列表"""
    def get_queryset(self):
        return Question.objects.get_correct_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CorrectAnsweredQuestionListView, self).get_context_data()
        context["active"] = "correct_answered"
        return context


class UncorrectAnsweredQuestionListView(QuestionListView):
    """没有正确答案的问题列表"""
    def get_queryset(self):
        return Question.objects.get_uncorrect_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UncorrectAnsweredQuestionListView, self).get_context_data()
        context["active"] = "uncorrect_answered"
        return context


class QuestionCreateView(LoginRequiredMixin, CreateView):
    """用户提问"""
    model = Question
    template_name_suffix = "_create_form"
    template_name = "quora/question_create_form.html"
    form_class = QuestionForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "问题已发表！")
        return reverse_lazy("quora:all-questions")


class QuestionDetailView(DetailView):
    """问题详情页"""
    model = Question
    context_object_name = 'question'
    template_name = 'quora/question_detail.html'
    query_pk_and_slug = True
    pk_url_kwarg = 'pk'
    slug_url_kwarg = 'slug'


class AnswerCreateView(LoginRequiredMixin, CreateView):
    """回答问题"""
    model = Answer
    fields = ['content']
    template_name_suffix = '_create_form'
    template_name = 'quora/answer_create_form.html'

    def get_context_data(self, **kwargs):
        context = super(AnswerCreateView, self).get_context_data()
        context['question'] = Question.objects.get(pk=self.kwargs['question_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(AnswerCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "答案已提交")
        return reverse_lazy("quora:question_detail", kwargs={"pk": self.kwargs['question_id'],
                                                             "slug": self.kwargs['question_slug']})


@login_required
@ajax_required
@require_http_methods(["POST"])
def question_vote(request):
    """给问题投票，AJAX POST请求"""
    question_id = request.POST["questionId"]
    value = True if request.POST["value"] == 'U' else False  # 'U'表示赞成，'D'表示反对
    question = Question.objects.get(pk=question_id)
    users = question.votes.values_list('user', flat=True)  # 当前问题的所有投票用户
    if request.user.pk in users and (question.votes.get(user=request.user).value == value):
        question.votes.get(user=request.user).delete()
    else:
        question.votes.update_or_create(user=request.user, defaults={"value": value})
    """
        # 1.用户首次操作，点赞/踩
        if request.user.pk not in users:
            question.votes.update_or_create(user=request.user, defaults={"value": value})

        # 2.用户已近赞过，要取消赞/踩一下
        elif question.votes.get(user=request.user).value:
            if value:
                question.votes.get(user=request.user).delete()
            else:
                question.votes.update_or_create(user=request.user, defaults={"value": value})

        # 3.用户已踩过，取消踩/赞一下
        else:
            if not value:
                question.votes.get(user=request.user).delete()
            else:
                question.votes.update_or_create(user=request.user, defaults={"value": value})
    """
    return JsonResponse({"votes": question.total_votes()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def answer_vote(request):
    """给回答投票，AJAX POST请求"""
    answer_id = request.POST["answerId"]
    value = True if request.POST["value"] == 'U' else False  # 'U'表示赞，'D'表示踩
    answer = Answer.objects.get(uuid=answer_id)
    users = answer.votes.values_list('user', flat=True)  # 当前回答的所有投票用户

    if request.user.pk in users and (answer.votes.get(user=request.user).value == value):
        answer.votes.get(user=request.user).delete()
    else:
        answer.votes.update_or_create(user=request.user, defaults={"value": value})

    return JsonResponse({"votes": answer.total_votes()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def accept_answer(request):
    """
    接受回答，AJAX POST请求
    已经被接受的回答用户不能取消
    """
    answer_id = request.POST["answerId"]
    answer = Answer.objects.get(pk=answer_id)
    # 如果当前登录用户不是提问者，抛出权限拒绝错误
    if answer.question.user.username != request.user.username:
        raise PermissionDenied
    answer.accept_answer()
    return JsonResponse({"status": "true"})

