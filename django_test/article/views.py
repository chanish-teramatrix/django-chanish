from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic.base import TemplateView 
from django.shortcuts import render_to_response
from article.models import Article
# from django.template import Context
# Create your views here.

def hello(request):
	name = 'chanish'
	responce = "<html><body> hi %s seems to be working fine"%name
	return HttpResponse(responce)
 
def hello_template(request):
	name = 'chanish'
 	t = get_template('hello.html')
 	html = t.render({'name': name})
 	return HttpResponse(html)

def practice_template(request):
 	name = 'nikhil'
 	return render_to_response('hello.html',{'name': name})

class HelloTemplate(TemplateView):
	template_name = 'hello_class.html'

 	def get_context_data(self, **kwargs):
 		context = super(HelloTemplate, self).get_context_data(**kwargs)
 		context['name'] = 'chanish'
 		return context


def articles(request):
	language = 'en-us' # stores in cookies
	session_language = 'en-us' # stores in session

	if 'lang' in request.COOKIES:	
		language = request.COOKIES['lang']

	if 'lang' in request.session:
		session_language = request.session['lang']

	return render_to_response('articles.html',
	  						   {'articles': Article.objects.all(),
	  						   'language': language,
	  						   'session_language': session_language})

#article_id = 1 has been choosen as default value.
def article(request, article_id = 1):
	return render_to_response('article.html',
							 {'article': Article.objects.get(id = article_id)})



def language(request, language='en-us'):
	responce = HttpResponse('setting language to %s' %language)

	responce.set_cookie('lang',language)

	request.session['lang'] = language
 
	return responce