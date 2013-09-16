#!/usr/bin/python3
#-*-coding:utf-8-*-

from  GetQueue import GetQueue
from DoFile import WriteFile
from DoFile import ReadFile
import time,datetime,os
from apscheduler.scheduler import Scheduler 

'''
@author: ljchu
2013-06-14
'''

class Monitor():
    def __init__(self):
        readFile = ReadFile()
        readFile.setFileName('config.txt')
        config=dict(readFile.ReadTxtBySpl())
        ActiveMqUrl='http://'+config['ActiveMqIp']+':8161/admin/queues.jsp'
        QueueName=config['QueueName']
        
        self.MonitorType=config['IntervalType']
        MonitorTime=config['IntervalTime']
        if int(MonitorTime) in [1,2,3,4,5,6,10,12,15,20,30,60]:
            self.MonitorTime=MonitorTime
        else:
            print('[ERROR] MonitorTime Illegal.') 
            return
        self.MonitorFileName=config['MonitorFileName']
        
        self.getQueue=GetQueue()
        self.getQueue.timeout=int(self.MonitorTime)/3
        self.getQueue.SetActiveMqUrl(ActiveMqUrl)
        self.getQueue.SetQueueName(QueueName)
        
        self.writeFile=WriteFile()
        self.writeFile.SetFileName(self.MonitorFileName)
        self.writeHead()
        
        self.sched = Scheduler()
        self.sched.daemonic = False
        print('Start Monitor....')
        if self.MonitorType=='ByMins':
            self.sched.add_cron_job(self.getMessage,minute='*/'+self.MonitorTime)
        elif self.MonitorType=='BySecs':
            self.sched.add_cron_job(self.getMessage,second='*/'+self.MonitorTime)
        self.sched.start()
        
    
    def __destroy__(self):
        self.sched.shutdown(wait=False)
    
    def writeHead(self):
        HeadTitle='Time\tNumberOfPendingMessages\tNumberOfConsumers\tMessagesEnqueued\tMessagesDequeued'
        print(HeadTitle)
        if os.path.exists(self.MonitorFileName) !=1:
            self.writeFile.WriteList(HeadTitle)
            
    def getMessage(self):
        b=self.getQueue.GetQueueMessage()
        Now=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.'+str(datetime.datetime.now().microsecond)
        if b==[]:
            ResultContent= Now+'\tTimeOut\tTimeOut\tTimeOut\tTimeOut' 
        elif b== None:
#            ResultContent= Now+'\tNone\tNone\tNone\tNone'
            self.__destroy__()
            return
        else:
            ResultContent=Now+'\t'+b[0]+'\t'+b[1]+'\t'+b[2]+'\t'+ b[3]
        print(ResultContent)
        self.writeFile.WriteList(ResultContent)
        
if __name__ == '__main__':  
    Monitor()
