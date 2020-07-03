from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView, CreateView, DetailView,UpdateView

from akatom.autils import AuthorRequiredMixin
from akatom.blogs.models import Article, ArticleCategory
from akatom.blogs.forms import ArticleForm


class ArticleListView(ListView):
    """已发布的文章列表"""
    model = Article
    paginate_by = 5
    context_object_name = 'article_list'
    template_name = "blogs/article_list.html"

    def get_queryset(self, **kwargs):
        return Article.objects.get_published()

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context['article_categories']= ArticleCategory.objects.all()
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context


class DraftListView(ArticleListView):

    def get_queryset(self, **kwargs):
        return Article.objects.get_drafts()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """创建文章"""
    model = Article
    form_class = ArticleForm
    template_name_suffix = '_create_form'
    template_name = "blogs/article_create_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleCreateView, self).form_valid(form)

    # success_url = reverse_lazy('blogs:list')
    def get_success_url(self):
        message = "您的文章已创建成功！"
        messages.success(self.request, message)
        return reverse_lazy('blogs:list')


class ArticleDetailView(DetailView):
    """文章详情页"""
    model = Article
    template_name = 'blogs/article_detail.html'
    context_object_name = 'article'


class ArticleUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """用户更新文章"""
    model = Article
    form_class = ArticleForm
    template_name_suffix = '_update_form'
    template_name = 'blogs/article_update_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleUpdateView, self).form_valid(form)

    # success_url = reverse_lazy('blogs:list')
    def get_success_url(self):
        message = "您的文章已更新成功！"
        messages.success(self.request, message)
        return reverse_lazy('blogs:detail', kwargs={'slug': self.get_object().slug})
