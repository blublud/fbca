'''
Created on Mar 10, 2013

@author: fan wei fang
'''
import urllib, json
from collections import deque

# retrieve_post('210455815693364')

class PostFetcher:

    commentStore={}   

#===============================================================================
# comments.fields(id,from,message,message_tags,created_time,likes.fields(id))
# Each comment is a dictionary:
#    + id:      commentId
#    + when:    when comment is created
#    + from:    the one who commented
#    + opt. tags: [taggedIds]
#    + opt. likes:[likeIds]
#===============================================================================

    def submit(self, postId):
        
        url = 'http://graph.facebook.com/' + postId +'/comments?fields=id,from,message,message_tags,created_time,likes.fields(id)'
        
        #should have checked if existence of postId.
        if postId not in self.commentStore: 
            self.commentStore[postId] = deque([])
        
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
            self.commentStore[postId].extend(comments)

    def getcomment(self, postId):
        if postId in self.commentStore and len(self.commentStore[postId]):
            return self.commentStore[postId].popleft()
        else:
            return None
