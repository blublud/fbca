# Create your views here.

from django.http import HttpResponse
from django.template.loader import get_template  
from django.template import Context
from dataaccess.fbdata import getPostInPage
from dataaccess.fbdata import getCommentInPost
from dataaccess.fbdata import getPostById
from hotcomment.graph import builder

def pagelist(request):
    
    template = get_template('pagelist.html')
    pagelist=[{'url':'/postlist?pageId=15704546335', 'name': 'Fox News'},
              {'url':'/postlist?pageId=5550296508', 'name': 'CNN'}]
    
    c = Context({'key':'val', 'pagelist': pagelist})
    return HttpResponse(template.render(c))

def postlist(request):    

    pageId = request.GET.get('pageId',None)            

    postListData = getPostInPage(pageId)
    postList = []
    for postData in postListData:
        post = {}
        post['imgUrl']=postData.get('picture','http://www.facebook.com/?ref=logo')
        post['message'] = postData['message']
        post['postUrl'] = '/postDetails?postId=' + postData['id']
        post['likes'] = postData['likes']['count']
        post['comments'] = postData['comments']['count']
        post['shares'] = postData['shares']['count']
        postList.append(post)
        
    template = get_template('postlist.html')
    c = Context({'key':'val','postList':postList})
    return HttpResponse(template.render(c))

def postDetails(request):
    postId = request.GET.get('postId',None)
    post = getPostById(postId)
    
    cmnts = getCommentInPost(postId)    
    b = builder()
    hotCmnts = b.getnHotCmnts(postId)
    refs = b.getCmntReferences(hotCmnts)
    for cmnt in cmnts:
        if cmnt['id'] in hotCmnts:
            cmnt['hot'] = hotCmnts.index(cmnt['id']) + 1
            cmnt['ref'] = refs[cmnt['id']]
        else:
            cmnt['hot'] = 0
            
    template = get_template('commentlist.html')
    c = Context({'key':'val','commentList':cmnts, 'hotCmnts':hotCmnts,'post':post})
    return HttpResponse(template.render(c))
