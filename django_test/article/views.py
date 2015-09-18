from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic.base import TemplateView 
from django.shortcuts import render_to_response
from article.models import Article
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
# from forms import MyRegistrationForm
from forms import ArticleForm
# from django.template import Context
# Create your views here.

def hello(request):
	name = 'chanish'
	response = "<html><body> hi %s seems to be working fine"%name
	return HttpResponse(response)
 
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
	response = HttpResponse('setting language to %s' %language)

	response.set_cookie('lang',language)

	request.session['lang'] = language
 
	return response

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html',c)

def auth_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = auth.authenticate(username = username , password = password)

	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect('/accounts/loggedin')
	else:
		return HttpResponseRedirect('/accounts/invalid')

def loggedin(request):
	return render_to_response('loggedin.html',
							{'full_name' : request.user.username})

def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')


def register_user(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/register_success')

	args = {}
	args.update(csrf(request))

	args['form'] = MyRegistrationForm ()   
	print args
	return render_to_response('register.html', args)

def register_success(request):
	return render_to_response('register_success.html')



def create(request):
	if request.POST:
		form = ArticleForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/articles/all')

	else:
		form = ArticleForm()

	args = {}
	args.update(csrf(request))

	args['form'] = form
	return render_to_response('create_article.html', args)

def like_article(request,article_id):
	if article_id:
		a = Article.objects.get(id = article_id)
		count = a.likes
		count = count+1
		a.likes = count
		a.save()

	return HttpResponseRedirect('/articles/get/%s' %article_id)