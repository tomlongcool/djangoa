from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # path("news/", TemplateView.as_view(template_name="pages/news.html"), name="news"),
    # path("blogs/", , name="blogs"),
    # path("quora/", TemplateView.as_view(template_name="pages/quora.html"), name="quora"),
    path("chat/", TemplateView.as_view(template_name="pages/chat.html"), name="chat"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("akatom.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # 新闻版块的路由
    path("news/", include("akatom.news.urls", namespace="news")),
    # 个人博客
    path("blogs/", include("akatom.blogs.urls", namespace="blogs")),
    # 问答版块
    path("quora/", include("akatom.quora.urls", namespace="quora")),


    # 第三方app的路由
    re_path(r'mdeditor/',include('mdeditor.urls')),
    re_path(r'^comments/', include('django_comments.urls')),
    path('markdownx/',include('markdownx.urls')),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
