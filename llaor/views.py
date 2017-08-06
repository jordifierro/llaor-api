import json

from django.http import HttpResponse
from django.views import View


class ViewWrapper(View):

    factory = None

    def get(self, request, *args, **kwargs):
        kwargs.update(request.GET.dict())
        body, status = self.factory.create(request).get(**kwargs)
        return HttpResponse(json.dumps(body), status=status, content_type='application/json')
