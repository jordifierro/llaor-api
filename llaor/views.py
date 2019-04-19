import json

from django.http import HttpResponse
from django.views import View


class ViewWrapper(View):

    view_creator_func = None

    def get(self, request, *args, **kwargs):
        kwargs.update(request.GET.dict())
        body, status = self.view_creator_func(request).get(**kwargs)
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')
