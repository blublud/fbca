'''
Created on Mar 18, 2013

@author: fan wei fang
'''
from wwwfront.facebook import get_app_access_token
import urllib, json
from collections import deque

appId='151424291689079'
appSecret='e261f25d83fa8649d4442df584824a7a'

def getPostInPage(pageId):
    
    accessToken = get_app_access_token(appId, appSecret)
    
    url = 'https://graph.facebook.com/' + pageId +'?access_token=' + accessToken + '&fields=posts'
    url_data = urllib.urlopen(url)
    response = json.load(url_data)    
    postListData = response['posts']['data']
    return postListData

commentStore={}

def getPostById(postId):
    accessToken = get_app_access_token(appId, appSecret)    
    url = 'https://graph.facebook.com/' + postId +'?access_token=' + accessToken + '&fields=picture,message'
    url_data = urllib.urlopen(url)
    response = json.load(url_data)    
    return response
    

def getCommentInPost(postId, forceFresh=True):    
    
    if forceFresh==False and postId in commentStore:
        return commentStore[postId]
    
    url = 'http://graph.facebook.com/' + postId +'/comments?fields=id,from,message,like_count,message_tags,created_time,likes.fields(id)'
    
    #should have checked if existence of postId. 
    commentStore[postId] = []
    
    more = True        
    while more:
        
        url_data = urllib.urlopen(url)
        dat = json.load(url_data)            
        
        #error handling
        if 'error' in dat:
            break
        
        if 'next' in dat['paging']:
            url = dat['paging']['next']
        else:
            more=False
        #fetched comments
        comments =dat['data'] 
        commentStore[postId].extend(comments)
    
    return commentStore[postId]