#!/usr/bin/python3
#-*-coding:utf-8-*-
import re
import urllib
from urllib.request import urlopen  
'''
@author: ljchu
2013-06-09
'''
class GetQueue:
    '''
    @return: list of queue message.
    @param ActiveMqUrl:the URI of the ActiveMq
    @param QueueName:the name of the queue
    '''
    def __init__(self):
        self.url=''
        self.QueueName=''
        self.pageDoc=''
        self.timeout=0
    
    def SetActiveMqUrl(self,ActiveMqUrl):
        self.url=ActiveMqUrl
        
    def SetQueueName(self,QueueName):
        self.QueueName=QueueName
    
    def ParserWebHtml(self):
        try:
            pageDoc = urlopen(self.url,timeout=self.timeout).read().decode("utf-8")
        except Exception as e:
            print(e)
            str_e=str(e)
            if str_e.find('timed') != -1:
                return 1
            else:
                return 2
        else:
            self.pageDoc=pageDoc
        
    def GetQueueMessageList(self):
        a=self.ParserWebHtml()
        if a==1:
            self.QueueMessageList=[]
            return
        elif a == 2:
            self.QueueMessageList=None
            return
        str=self.QueueName+'</a></td>'
        #get the start position of the queue message
        StartPos=self.pageDoc.find(str)
        if StartPos<0:
            print('[WARN]:Can not find the Queue:'+self.QueueName)
            self.QueueMessageList=None
            return
        #set the end position
        EndPos=StartPos+100
        a_string=self.pageDoc[StartPos:EndPos].replace('\n','').rstrip()
        #get the begin and end position of every no
        index_begin = -1
        index_end = -1
        
        pos_begin=[]
        pos_end=[]
        while True:
            index_begin = a_string.find('<td>',index_begin+1)
            index_end = a_string.find('</td>',index_end+1)
            if index_begin==-1 or index_end==-1:
                break
            pos_begin.append(index_begin)
            pos_end.append(index_end)
        for i in range(len(pos_begin)-1):
            self.QueueMessageList.append(a_string[pos_begin[i]+4:pos_end[i+1]])

    def GetQueueMessage(self):
        self.QueueMessageList=[]
        self.GetQueueMessageList()
        return self.QueueMessageList
