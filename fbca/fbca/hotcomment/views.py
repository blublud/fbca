# Create your views here.
from django.http import HttpResponse
from graph import builder
import json

def response(request):
    
    postId= request.GET.get('postId','')
    
    b = builder()
    hotCmnts = b.getnHotCmnts(postId)
    
    return HttpResponse(json.dumps(hotCmnts), content_type='application/json')