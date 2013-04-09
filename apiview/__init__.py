from datetime import datetime
import traceback
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.core.serializers import serialize
from django.db.models.query import QuerySet

import json
from django.utils.functional import Promise
from django.utils.encoding import force_text

class LazyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return json.loads(serialize('json', obj))
        elif isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


class api_view(object):

	def __init__(self,show_run_time=True,usage=None,show_usage=True,jsonp=True):
		self.show_run_time = show_run_time
		self.run_time = 0
		self.ud = usage
		self.show_usage = show_usage
		self.jsonp = jsonp
		self.mime_type = "application/json"
		self.response = HttpResponse

	def usage(self):
		def v(tup):
			if type(tup) in (tuple,list,set):
				req = tup[0]
				details = tup[1]
			else:
				req = True
				details = tup
			return {
				'Required': req,
				'Details': details
			}
		if self.ud is not None:
			return dict((k,v(self.ud[k])) for k in self.ud.keys())
		else: 
			return None

	def validated(self):
		if self.ud is None: return True
		for k in self.ud.keys():
			if (type(self.ud[k]) not in (tuple,list,set) or self.ud[k][0])\
				and self.request.REQUEST.get(k) is None:
				return False
		return True

	def render(self,data=None):
		if data is None:
			data = {}
		elif not isinstance(data,dict):
			data = { 'data': data }

		if self.show_run_time: data['run_time'] = self.run_time
		if self.show_usage and self.ud: data['usage'] = self.usage()

		body = json.dumps(data,indent=2,cls=LazyEncoder)
		if 'callback' in self.request.GET and self.jsonp:
			body = "{callback}({json})".format(
					callback=self.request.GET['callback'],
					json=body
					)
			self.mime_type = "application/javascript"


		return self.response(body,content_type=self.mime_type)


	def __call__(self,func):
		def view(request,*args,**kwargs):
			self.request = request
			result = {}
			if self.usage and not self.validated():
				self.response = HttpResponseBadRequest
			else:
				try:
					start = datetime.now()
					result['data'] = func(request,*args,**kwargs)
					self.run_time = (datetime.now()-start).total_seconds()
				except:
					self.response = HttpResponseServerError
					result = {
						'exception': traceback.format_exc()
					}

			return self.render(result)

		return view

