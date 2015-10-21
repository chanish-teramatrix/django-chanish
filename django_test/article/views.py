import json
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from article.models import Article, Signal
from todo.models import User
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django_datatables_view.base_datatable_view import BaseDatatableView
from forms import ArticleForm, ProfileForm, SignalForm, EmailForm
from datetime import datetime
from django.db.models import Q
from django.views.generic.edit import FormView, View
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


# from django.template import Context
# Create your views here.

def hello(request):
    name = 'chanish'
    response = "<html><body> hi %s seems to be working fine" % name
    return HttpResponse(response)


def hello_template(request):
    name = 'chanish'
    t = get_template('hello.html')
    html = t.render({'name': name})
    return HttpResponse(html)


def practice_template(request):
    name = 'nikhil'
    return render_to_response('hello.html', {'name': name})


class HelloTemplate(TemplateView):
    template_name = 'hello_class.html'

    def get_context_data(self, **kwargs):
        context = super(HelloTemplate, self).get_context_data(**kwargs)
        context['name'] = 'chanish'
        return context


def articles(request):
    p = request
    pp = p.GET
    language = 'en-us'  # stores in cookies
    session_language = 'en-us'  # stores in session

    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']

    if 'lang' in request.session:
        session_language = request.session['lang']

    args = {}
    args.update(csrf(request))

    args['articles'] = Article.objects.all()
    args['language'] = language
    args['session_language'] = session_language
    args['request'] = p
    args['requestGet'] = pp
    print "ARticle model"
    print Article.objects.all()
    return render_to_response('articles.html', args)


# article_id = 1 has been choosen as default value.
def article(request, article_id=1):
    return render_to_response('article.html',
                              {'article': Article.objects.get(id=article_id)})


def language(request, language='en-us'):
    response = HttpResponse('setting language to %s' % language)

    response.set_cookie('lang', language)

    request.session['lang'] = language

    return response


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
    return render_to_response('loggedin.html',
                              {'full_name': request.user.username})


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

    args['form'] = MyRegistrationForm()
    print args
    return render_to_response('register.html', args)


def register_success(request):
    return render_to_response('register_success.html')


def create(request):
    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        print "request.FILES in views.py", request.FILES
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/articles/all')

    else:
        form = ArticleForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form
    return render_to_response('create_article.html', args)


def create_profile(request):
    if request.POST:
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect('/articles/all')
    else:
        profile_form = ProfileForm()

    args = {}
    args.update(csrf(request))

    args['profile_form'] = profile_form
    return render_to_response('user_information.html', args)


def like_article(request, article_id):
    if article_id:
        a = Article.objects.get(id=article_id)
        count = a.likes
        count = count + 1
        a.likes = count
        a.save()

    return HttpResponseRedirect('/articles/get/%s' % article_id)


def search_titles(request):
    print "request.method in views.py line 147", request.method
    if request.method == "POST":
        search_text = request.POST['search_text']

    else:
        search_text = ''

    articles = Article.objects.filter(title__contains=search_text)

    return render_to_response('ajax_search.html', {'articles': articles})


class dbview(TemplateView):
    template_name = 'dbtable.html'

    def get_context_data(self, **kwargs):
        context = {}
        datatable_headers = [
            {'mData': 'title', 'sTitle': 'Title', },
            {'mData': 'body', 'sTitle': 'Body'},
            {'mData': 'pub_date', 'sTitle': 'Published Date'}

        ]
        context['datatable_headers'] = json.dumps(datatable_headers)
        return context


class dbdata(BaseDatatableView):
    model = Article

    columns = [
        'id',
        'title',
        'body',
        'pub_date',
    ]

    order_columns = [
        'title',
        'body',
        'pub_date'
    ]

    @property
    def _querydict(self):
        if self.request.method == 'POST':
            return self.request.POST
        else:
            return self.request.GET

    def filter_queryset(self, qs):
        """
        If search['value'] is provided then filter all searchable columns using istartswith
        """
        if not self.pre_camel_case_notation:
            # get global search value
            search = self.request.GET.get('search[value]', None)
            col_data = ['body']
            q = Q()
            for col in col_data:
                # apply global search to all searchable columns
                q |= Q(**{'{0}__istartswith'.format(col): search})
            qs = qs.filter(q)
        return qs

    def get_order_columns(self):
        # returns the order_columns we have declared above
        return self.order_columns

    def get_columns(self):
        return self.columns

    def ordering(self, qs):
        print "ordering is working"
        sorting_cols = 0
        if self.pre_camel_case_notation:
            try:
                sorting_cols = int(self._querydict.get('iSortingCols', 0))
            except ValueError:
                sorting_cols = 0
        else:
            sort_key = 'order[{0}][column]'.format(sorting_cols)
            # print "---------self._querydict(sort_key)----------"
            # print sort_key
            # print self._querydict.get(sort_key)
            # print "---------self._querydict(sort_key)----------"

            while sort_key in self._querydict:
                sorting_cols += 1
                sort_key = 'order[{0}][column]'.format(sorting_cols)

        order = []
        order_columns = self.get_order_columns()

        for i in range(sorting_cols):
            # sorting columns
            sort_dir = 'asc'
            try:
                if self.pre_camel_case_notation:
                    sort_col = int(self._querydict.get('iSortCol_{0}'.format(i)))
                    # sorting order
                    sort_dir = self._querydict.get('sSortDir_{0}'.format(i))
                else:
                    sort_col = int(self._querydict.get('order[{0}][column]'.format(i)))
                    # sorting order
                    sort_dir = self._querydict.get('order[{0}][dir]'.format(i))
            except ValueError:
                sort_col = 0

            sdir = '-' if sort_dir == 'desc' else ''
            sortcol = order_columns[sort_col]

            if isinstance(sortcol, list):
                for sc in sortcol:
                    order.append('{0}{1}'.format(sdir, sc.replace('.', '__')))
            else:
                order.append('{0}{1}'.format(sdir, sortcol.replace('.', '__')))

        if order:
            return qs.order_by(*order)
        return qs

    # max_display_length = 3

    def paging(self, qs):
        if self.pre_camel_case_notation:
            limit = min(int(self._querydict.get('iDisplayLength', 10)),
                        self.max_display_length)
            start = int(self._querydict.get('start', 0))
        else:
            print "----line 263 article/views.py _querydict.get('length')-------"
            print self._querydict.get('length')
            limit = min(5, self.max_display_length)
            start = int(self._querydict.get('start', 0))

        if limit == -1:
            return qs
        offset = start + limit

        return qs[start:offset]

    def get_initial_queryset(self):
        qs = self.model.objects.all()
        return qs

    def prepare_results(self, qs):

        result = list()
        format = "%a %b %d %H:%M:%S %Y"
        for data in qs:
            temp_dict = {
                'title': data.title,
                'body': data.body,
                'pub_date': datetime.strftime(data.pub_date, format)
            }
            result.append(temp_dict)

        return result

    def get_context_data(self, *args, **kwargs):

        self.initialize(*args, **kwargs)

        qs = self.get_initial_queryset()

        # number of records before filtering
        total_records = qs.count()

        qs = self.filter_queryset(qs)

        # number of records after filtering
        total_display_records = qs.count()

        qs = self.ordering(qs)
        print "--query set before paging   line 311 article/views.py--"
        print qs
        print "------------------------------"
        qs = self.paging(qs)

        print "--query set after paging   line 316 article/views.py--"
        print qs
        print "------------------------------"

        aaData = self.prepare_results(qs)
        print "---qs---aaData "
        print aaData
        print "---------------"

        ret = {
            'sEcho': int(self._querydict.get('sEcho', 0)),
            'iTotalRecords': total_records,
            'iTotalDisplayRecords': total_display_records,
            'aaData': aaData
        }

        return ret


def signaltest(request):
    if request.POST:
        signal_form = SignalForm(request.POST)
        signal_form.save()
        return HttpResponseRedirect('/articles/all')

    else:
        signal_form = SignalForm()

    args = {}
    args.update(csrf(request))
    args['signal_form'] = signal_form
    return render_to_response("signaltest.html", args)


# def email(request):
# 	if request.POST:
# 		email_form =object EmailForm(request.POST)
# 		if email_form.is_valid():
# 			# subject = email_form.cleaned_data['subject']
# 			# message = email_form.cleaned_data['message']
# 			# from_email = email_form.cleaned_data['from_email']
# 			# to_email = email_form.cleaned_data['to_email']
#
# 			# email_form.save()
# 			print "\n in views.py email funcition sending email \n"
# 			# send_email(subject,message,from_email,to_email)
# 			return HttpResponseRedirect('/articles/thanks/')
# 		else:
# 			print email_form.errors
#
# 	else:
# 		email_form = EmailForm()
#
# 	args={}
# 	args.update(csrf(request))
# 	args['form'] = email_form
# 	return render_to_response('email_form.html',args)

class Email(FormView):
    template_name = 'email_form.html'
    form_class = EmailForm
    success_url = '/articles/thanks/'

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.is_valid():

            subject = request.POST.get('subject')
            message = request.POST.get('message')
            from_email = request.POST.get('from_email')
            recipient_list = [request.POST.get('to_email')]

            # sending mail using above attributes
            send_mail(subject, message, from_email, recipient_list,
                      fail_silently=False)

            return self.form_valid(form)


        else:
            return self.form_invalid(form)


def error(request, **kwargs):
    return render_to_response('error.html', **kwargs)


class Mailtest(View):
    success_url = '/articles/thanks/'

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Mailtest, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):

        # From: To send the mail sender's email.
        from_email = self.request.POST.get('from_email', None)

        # To: mail id where to send mail.
        to_email = self.request.POST.get('to_email', None)

        # Subject: Mail subject
        subject = self.request.POST.get('subject', None)

        # Message: Email Message will be here.
        message = self.request.POST.get('message', None)

        # Attachments: Mail attachments if any.
        attachments = None
        try:
            attachments = request.FILES.get('attach', None)

        except Exception as e:
            print "in exception"
            logger.exception(e.message)


        # Result: Response to be returned.
        result = {
            "success": 0,
            "message": "Failed: Something is wrong here.",
            "data": {
                "from": from_email,
                "to": to_email
            }
        }

        # Error Message.
        error_messages = ""
        if not to_email:
            # error_message generation when 'to_email' value not provided:
            error_messages = "Please specify email id of sender. \n"

        if not from_email:
            # error_message generation when 'from_email' value not provided:
            error_messages += "Mail sender's id is not given \n"

        if error_messages:
            # succes bit has changed to '1'
            # success = 1 : mail has not been send
            result['success'] = 1

            # result['message'] : expected errors has been stored their
            result['message'] = error_messages
            print '*' * 30
            print result
            print '*' * 30
            HttpResponse(json.dumps(result))

        else:
            # TODO: correct to_email here used list for testing purpose
            mail = EmailMessage(subject, message, from_email, [to_email])
            # Handling mail without an attachment
            if not attachments:
                mail.send()
            # Handling mail with attachments
            else:
                mail.attach(attachments.name, attachments.read(),
                            attachments.content_type)
                mail.send()
            print '*' * 30
            print result
            print '*' * 30
            HttpResponse(json.dumps(result))


def thanks(request):
    return render_to_response('thanks.html')
