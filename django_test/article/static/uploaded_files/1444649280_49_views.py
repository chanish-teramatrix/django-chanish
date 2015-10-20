import json
# from djago impoort
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView, DeleteView
from django.views.generic.edit import CreateView, FormView
from application.models import Task, Actionlogs
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.core.urlresolvers import reverse_lazy
from application.forms import Newtaskform

# Create your views here.
class TaskList(TemplateView):

	template_name = 'application/template_list.html'

	def get_context_data(self, **kwargs):
		context = super(TaskList, self).get_context_data(**kwargs)
		datatable_headers = [
			{'mData': 'status', 'sTitle': 'Status', 'sWidth': 'auto', 'bSortable': False},
			{'mData': 'name', 'sTitle': 'Name', 'sWidth': 'auto', 'bSortable': True},
			{'mData': 'dead_date', 'sTitle': 'dead_dateline', 'sWidth': 'auto', 'bSortable': True},
			{'mData': 'actions', 'sTitle': 'Actions', 'sWidth': 'auto', 'bSortable': False},
		]
		context['datatable_headers'] = json.dumps(datatable_headers)

		return context
	# def get_context_data(self, **kwargs):
	# 	context = dict()
	# 	context = super(TaskList, self).get_context_data(**kwargs)
	# 	datalist = Task.objects.all()
	# 	print "*************"
	# 	print datalist
	# 	print "*************"
	# 	context['datalist'] = datalist
	# 	return context

class TaskListingTable(BaseDatatableView):

	model = Task
	columns = ["id", "status", "name", "dead_date"]
	order_columns = ["name", "dead_date"]

	def get_initial_queryset(self):
		qs = self.model.objects.all()
		return qs

	def prepare_resuts(self, qs):
		resultset = []
		for item in qs:
			data_dict = {
				"name" : "",
				"status" : "",
				"dead_date" : "",
				"id" : "",
				"actions" : ""
			}
			
			checked = ''

			if int(item.status):
				checked = 'checked="checked"'

			data_dict["name"] = item.name
			data_dict["id"] = item.id
			data_dict["dead_date"] = item.dead_date.strftime("%Y-%m-%d %H:%M:%S")
			data_dict["status"] = '<input type="checkbox" name="status_checkbox" pk="'+str(item.id)+'" class="status_checkbox" '+checked+'/>'
			delete_url = reverse_lazy('Deletetask', kwargs = {'pk': item.id})
			data_dict["actions"] = '<a href = "%s"> DELETE </a>' % delete_url
			resultset.append(data_dict)

		return resultset

	def get_context_data(self, *args, **kwargs):

		self.initialize(*args, **kwargs)

		qs = self.get_initial_queryset()

		# number of records before filtering
		total_records = qs.count()

		qs = self.filter_queryset(qs)

		# number of records after filtering
		total_display_records = qs.count()

		qs = self.ordering(qs)
		qs = self.paging(qs)

		if not qs and isinstance(qs, ValueQuerySet):
			qs=list(qs)

		aaData  = self.prepare_resuts(qs)

		ret = {
			'sEcho': int(self._querydict.get('sEcho', 0)),
			'iTotalRecords': total_records,
			'iTotalDisplayRecords': total_display_records,
			'aaData': aaData
		}

		return ret

class UserLogDeleteMixin(object):
	"""
    View mixin which log the user action on delete.
    """
	def delete(self, request, *args, **kwargs):
		"""
		overide the DeleteView for saving user logs
		"""
		print "heehhehhehehheeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
		obj = self.get_object()
		task_name = getattr(obj, 'name')
		action = "A task {0} is deleted".format(task_name)
		Actionlogs.objects.create(action = action)
		return super(UserLogDeleteMixin, self).delete(request, *args, **kwargs)
		
class TaskDelete(UserLogDeleteMixin, DeleteView):
	model = Task
	success_url = reverse_lazy('TaskList')
	template_name = 'application/application_delete.html'


class UserLogsListing(TemplateView):
	template_name = 'application/userlogs.html'

	def get_context_data(self, **kwargs):
		context = super(UserLogsListing, self).get_context_data(**kwargs)
		logs = Actionlogs.objects.all()
		context['logs'] = logs
		return context
# One method for input of form
class NewTask(CreateView):
	model = Task
	fields = ['name', 'dead_date']
	template_name = 'application/newtask.html'

# Second Method of input of form
# Form class normal 

# Third method tough one
# class NewTask(CreateView):
# 	model = Task
# 	template_name = 'application/newtask.html'
# 	form_class = Newtaskform
# 	success_url = reverse_lazy('TaskList')
# 	# def form_valid(self, request):
# 	# 	return super(NewTask, self).form_valid(request)
# 	def get(self, request, *args, **kwargs):
# 		form_class = self.get_form_class()
# 		form = self.get_form(form_class)
# 		return self.render_to_response(self.get_context_data(form = form))

# 	def post(self, request, *args, **kwargs):
# 		form_class = self.get_form_class()
# 		form = self.get_form(form_class)	
# 		if form.is_valid():
# 			form.save(commit=False)
# 			form.save()
# 			return HttpResponseRedirect(NewTask.success_url)
# 		else:
# 			return self.render_to_response(self.get_context_data(form = form))	