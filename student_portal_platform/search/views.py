import json

from django.http import HttpResponse
from django.contrib.auth.models import User

def search(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        print q
        users = User.objects.filter(first_name__contains=q)
        print users
        searchresults = []
        data = {}
        for user in users:
            data['id'] = str(user.id)
            data['name'] = user.first_name
            searchresults.append(data)
        return HttpResponse(json.dumps(searchresults), content_type="application/json")
