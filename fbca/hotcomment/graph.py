'''
Created on Mar 12, 2013

@author: fan wei fang
'''
from scipy.sparse.linalg import spsolve, eigs
from scipy.linalg import lu_solve
from numpy import eye, nonzero, ones

from dataaccess.fbdata import getCommentInPost
import logging, os
from hotcomment import utils
from time import clock
 
GRAPH_SIZE=1000
FILE_STOP_WORDS = os.path.join (os.path.dirname(os.path.abspath(__file__)), 'english.stop')

class builder:
    
    skipWords = set()
    f = open(FILE_STOP_WORDS)
    for stopword in f.read().splitlines():
        skipWords.add(stopword)
    
    logger = logging.getLogger('builder')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('dbg.log')
    logger.addHandler(fh)
    logwriter = utils.LoggerWriter(logger, logging.DEBUG)
    
    prg = eye(1) 
    cmntIdMap = []
    cmnts_window =[]

    likes_window = {}
    users_window = {}
    voc_window = {}

    def buildgraph(self, postId):
        
        cmnts = getCommentInPost(postId, False)
        size = len(cmnts)
        self.prg = eye(size) 
            
        
        for cmnt in cmnts:            
            #replace native fb comment Id by local comment index in cmntIdMap
            cmntIdx = len(self.cmntIdMap)            
            self.cmntIdMap.append(cmnt['id'])
            
            #put comment into comment_window
            self.cmnts_window.append({'message':cmnt['message'], 'evicted':False})            
            
            #put the commentor into user_window
            cmnterId = cmnt['from']['id']            
            if cmnterId in self.users_window:
                self.users_window[cmnterId].append(cmntIdx)
            else:
                self.users_window[cmnterId] = [cmntIdx]
            
            #get the likes and fill into like_window
            likes= cmnt.get('likes',{}).get('data',[])
            for l in likes:
                if l['id'] in self.likes_window:
                    self.likes_window[l['id']].append(cmntIdx)
                else:
                    self.likes_window[l['id']]= [cmntIdx]
            
            #voc window here
            text = cmnt['message'].lower()
            words = text.split()
            voc_link ={}#cmntIdx:count count the common word between current comment and previous ones
            for w in words:
                if w not in self.skipWords:
                    if w in self.voc_window:
                        for idx in self.voc_window[w]: voc_link[idx] = voc_link.get(idx, 0) + 1
                        self.voc_window[w].append(cmntIdx)
                    else:
                        self.voc_window[w] = [cmntIdx]
            
            #build the graph
            #using like info
            if cmnterId in self.likes_window:
                for likedIdx in self.likes_window[cmnterId]: 
                    self.prg[likedIdx, cmntIdx] += 1
    
            #using voc info
            for idx, commonwordcount in voc_link.items():
                #do filtering here                 
                self.prg[idx, cmntIdx] += 1
    
        #end while 

#===============================================================================
# b = builder()
# b.build('10151574324009369')
# print b
#===============================================================================

    def getnHotCmnts(self, postId, nCmnts = 5):
        self.buildgraph(postId)
        hot_cmnts = self.findCentralCmnt(nCmnts)
        return hot_cmnts
    
    def getCmntReferences(self, hotCmnts):
        references = {}                
        for cmnt in hotCmnts:            
            hotIdx = self.cmntIdMap.index(cmnt)
            idxRef = nonzero(self.prg[hotIdx])[0]
            references[cmnt]  = [self.cmntIdMap[idx] for idx in idxRef]
        return references
        
    def findCentralCmnt(self, nCmnts):
        
        cmnt_count = len(self.cmntIdMap)
        eig = eigs(self.prg, return_eigenvectors =False, maxiter=10, tol=1E-5)
        eig = eig[0].real
        eig = 1/eig
        
        one = ones(cmnt_count)
        m = eye(cmnt_count) - eig*self.prg
        cmnts_ranking = lu_solve((m, one), one)
        hot_cmnts = []
        
        for i in xrange(nCmnts):
            m = max(enumerate(cmnts_ranking),key=lambda x: x[1])[0]            
            if m > cmnt_count: break            
            hot_cmnts.append(self.cmntIdMap[m])
            cmnts_ranking[m] = 0 
        
        return hot_cmnts
