from django.conf.urls import include, url
# from views import Email
import views as views
# article_resource = ArticleResource()

urlpatterns = [
    url(r'^all/$', 'article.views.articles'),
    url(r'^get/(?P<article_id>\d+)/$', 'article.views.article'),
    url(r'^language/(?P<language>[a-z\-]+)/$', 'article.views.language'),
    url(r'^create/$', 'article.views.create'),
    url(r'^like/(?P<article_id>\d+)/$', 'article.views.like_article'),
    url(r'^search/$', 'article.views.search_titles'),
    url(r'^userprofile/$', 'article.views.create_profile', name="article_user_form"),
    # signal testing
    url(r'^signaltest/$', 'article.views.signaltest', name='singal_test'),
    url(r'email/$', views.Email.as_view(), name = 'email'),
    url(r'thanks/$', 'article.views.thanks', name='thanks'),
    url(r'mailtest/$', views.Mailtest.as_view(), name='mail_test')

]
