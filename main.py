#-*-coding:utf-8-*-

from  GetQueue import GetQueue
from DoFile import WriteFile
from DoFile import ReadFile
import time,datetime,os

'''
@author: ljchu
2013-06-14
'''

def main():
    readFile = ReadFile()
    readFile.setFileName('config.txt')
    config=dict(readFile.ReadTxtBySpl())
#    print(config)
    ActiveMqUrl='http://'+config['ActiveMqIp']+':8161/admin/queues.jsp'
    QueueName=config['QueueName']
    SleepTime=int(config['IntervalTime'])
    CycleTimes=int(int(config['MonitorTime'])/int(config['IntervalTime']))
#    print(CycleTimes)
    MonitorFileName=config['MonitorFileName']
    
    
    a=GetQueue()
    a.SetActiveMqUrl(ActiveMqUrl)
    a.SetQueueName(QueueName)
    c=WriteFile()
    c.SetFileName(MonitorFileName)
    print('Start Monitor....')
    HeadTitle='Time\tNumberOfPendingMessages\tNumberOfConsumers\tMessagesEnqueued\tMessagesDequeued'
    print(HeadTitle)
    if os.path.exists(MonitorFileName) !=1:
        c.WriteList(HeadTitle)
    for i in range(CycleTimes):
        b=a.GetQueueMessage()
        Now=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.'+str(datetime.datetime.now().microsecond)
        ResultContent=Now+'\t'+b[0]+'\t'+b[1]+'\t'+b[2]+'\t'+ b[3]
        print(ResultContent)
        c.WriteList(ResultContent)
        time.sleep(SleepTime)
    print('Finished.')

if __name__ == '__main__':  
    main()
