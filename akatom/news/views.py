from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView
from akatom.autils import ajax_required, AuthorRequiredMixin
from akatom.news.models import News


class NewsListView(ListView):
    """新闻列表页"""
    queryset = News.objects.filter(reply=False).all()
    paginate_by = 5
    templates_name = 'news/news_list.html'
    context_object_name = 'news_list'


@login_required
@require_http_methods(["POST"]) #判断是否为POST请求
@ajax_required
def post_news(request):
    """发送动态ajax POST请求"""
    newsContent = request.POST['news_content'].strip()
    if newsContent:
        news = News.objects.create(user=request.user, content=newsContent)
        html = render_to_string('news/news_single.html', {'news':news,'request':request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空")


class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """删除一条新闻记录"""
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news:list') # 在项目的URLconf未加载前使用


@login_required
@require_http_methods(["POST"]) # 判断是否为POST请求
@ajax_required
def like(request):
    """点赞 ajax post响应请求"""
    news_id = request.POST['newsId']
    news = News.objects.get(pk=news_id)
    # 取消点赞或者添加赞
    news.switch_like(request.user)
    # 返回赞的数量
    return JsonResponse({"likers_count": news.likers_count()})

@login_required
@require_http_methods(["POST"]) #判断是否为POST请求
@ajax_required
def post_reply(request):
    """发送动态ajax POST请求"""
    replyContent = request.POST['replyContent'].strip()
    parentId = request.POST['newsid']  # 根据前端表单的name属性来取值
    parent = News.objects.get(pk=parentId)
    if replyContent:
        parent.reply_this(request.user, replyContent)
        return JsonResponse({'newsid': parent.pk,'replies_count': parent.replies_count()})
    else:
        return HttpResponseBadRequest("内容不能为空")




@ajax_required
@require_http_methods(["GET"])
def get_replies(request):
    """返回新闻的评论，AJAX GET请求"""
    news_id = request.GET['newsId']
    news = News.objects.get(pk=news_id)
    # render_to_string()表示加载模板，填充数据，返回字符串
    replies_html = render_to_string("news/reply_list.html", {"replies": news.get_children()})  # 有评论的时候
    return JsonResponse({
        "newsid": news_id,
        "replies_html": replies_html,
    })











