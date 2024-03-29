#!/usr/bin/python3
#-*-coding:utf-8-*-

import numpy as np
import pylab as pl
from DoFile import ReadFile
import sys,os
import matplotlib.font_manager

'''
@author: ljchu
2013-06-16
'''

class report():   
    '''
    draw report for activemq
    '''
    def __init__(self):
        self.fontSize=10
        
        self.Content_MessagesDequeued=[]
        self.Content_NumberOfPendingMessages=[]
        self.Content_NumberOfConsumers=[]
        self.Content_MessagesEnqueued=[]
        self.difference_Dequeued=[]
        self.difference_Enqueued=[]
        
        configFile=os.getcwd()+'\config.txt'
        
        if os.path.exists(configFile):
            self.configFile=configFile
        else:
            print('[ERROR 2] No such file or directory:',configFile)
            return
            
        readFile = ReadFile()
        readFile.setFileName(self.configFile)
        self.config=dict(readFile.ReadTxtBySpl())
        self.file=self.config['MonitorFileName']
        if os.path.exists(self.file)!=1:
            print('[ERROR 2] No such file or directory:',self.file)
            return
        self.creatReport()
    
    def setPoint(self,a_list):
        '''@return: a list with x and y Coordinate
        '''
        x=[]
        y=[]
        for i in range(len(a_list)):
            x9=i
            x.append(x9)
            y2=a_list[i]
            y.append(y2)
        return x,y
    
    def averageCalculator(self,a_list):
        '''
        @return: the average of a list
        '''
        t=0
        for i in a_list:
            t+=int(i)
        if len(a_list)!=0:
            a=t/len(a_list)
            return "%.2f" %a
        else:
            return 0

    def noZeroAverageCalculator(self,a_list):
        '''
        @return: the average of a list without zero
        '''
        b=[]
        for i in a_list:
            if i !=0:
                b.append(int(i))
        if len(b)!=0:
            a=sum(b)/len(b)
            return "%.2f" %a
        else:
            return 0

    def getMessageList(self):
        '''
        set the list of the queue
        '''
        line_no=0
        try:
            with open(self.file,encoding=sys.getfilesystemencoding())as a_file:
                for a_line in a_file:
                    line_no +=1
                    a_Content = a_line.rstrip().split('\t')
                    D_Content = a_Content[4]
                    if D_Content.find('MessagesDequeued')==-1:
                        if D_Content== 'TimeOut'or D_Content == 'None'and len(self.Content_MessagesDequeued)!=0:
                            self.Content_NumberOfPendingMessages.append(self.Content_NumberOfPendingMessages[-1])
                            self.Content_NumberOfConsumers.append(self.Content_NumberOfConsumers[-1])
                            self.Content_MessagesEnqueued.append(self.Content_MessagesEnqueued[-1])
                            self.Content_MessagesDequeued.append(self.Content_MessagesDequeued[-1])
                        else:
                            self.Content_NumberOfPendingMessages.append(a_Content[1])
                            self.Content_NumberOfConsumers.append(a_Content[2])
                            self.Content_MessagesEnqueued.append(a_Content[3])
                            self.Content_MessagesDequeued.append(a_Content[4])
                    else:
                        line_no +=1
        except Exception as e:
            print(e)
            return
        
        
    def getdifference(self):
            for j in range(1,len(self.Content_MessagesDequeued)):
                if self.Content_MessagesDequeued[j-1]=='None' or self.Content_MessagesDequeued[j-1]=='TimeOut':
                    self.difference_Dequeued.append(0)
                    self.difference_Enqueued.append(0)
                else:
                    self.difference_Enqueued.append(int(self.Content_MessagesEnqueued[j])-int(self.Content_MessagesEnqueued[j-1]))
                    self.difference_Dequeued.append(int(self.Content_MessagesDequeued[j])-int(self.Content_MessagesDequeued[j-1]))
    
    def draw_one_plot(self,x,y,color,Label):
        '''
        draw one line in a subplot
        '''
        # use pylab to plot x and y
        pl.plot(x, y,color,label=Label)
        
        pl.grid(True)
        p1_legend=pl.legend(loc=2,fancybox=True,prop=matplotlib.font_manager.FontProperties(size=self.fontSize))
        p1_legend.get_frame().set_alpha(0.3)
        
    def draw_two_plot(self,x,y,color,Label1,x2,y2,color2,Label2):
        '''
        draw two lines in a subplot
        '''
        # use pylab to plot x and y
        pl.plot(x, y,color,label=Label1)
        pl.plot(x2,y2,color2,label=Label2)
        
        pl.grid(True)
        p1_legend=pl.legend(loc=2,fancybox=True,prop=matplotlib.font_manager.FontProperties(size=self.fontSize))
        p1_legend.get_frame().set_alpha(0.3)
            
    def getMonitorTime(self):
        time=self.config['IntervalTime']
        IntervalType=self.config['IntervalType']
        if IntervalType=='BySecs':
            self.time=time+' seconds'
        elif IntervalType=='ByMins':
            self.time=time+' minutes'
    
    def creatReport(self):
        self.getMonitorTime()
        self.getMessageList()
        self.getdifference()
              
        pl.figure(1)
        ax1 = pl.subplot(311)
        ax2 = pl.subplot(312)
        ax3 = pl.subplot(313)
    
        #draw Messages Enqueued and Dequeued
        pl.sca(ax1)
        pl.title('Messages Enqueued and Dequeued')
        pl.ylabel('Number')
        if self.config['ReportMode']=='D':
            x11,y11=self.setPoint(self.Content_MessagesDequeued[1:])
            self.draw_one_plot(x11, y11,'r','$Dequeued$')
        elif self.config['ReportMode']=='E':
            x12,y12=self.setPoint(self.Content_MessagesEnqueued[1:])
            self.draw_one_plot(x12, y12,'black','$Enqueued$')
        else:
            x11,y11=self.setPoint(self.Content_MessagesDequeued[1:])
            x12,y12=self.setPoint(self.Content_MessagesEnqueued[1:])
            self.draw_two_plot(x11, y11,'r','$Dequeued$',x12,y12,'black','$Enqueued$')
    
        #draw Difference
        pl.sca(ax2)
        pl.title('Messages Difference (per '+self.time+' )')
        pl.ylabel('Number')
        if self.config['ReportMode']=='D':
            x21,y21=self.setPoint(self.difference_Dequeued)
            if self.config['IsCalZero']=='Z':
                average_Dequeued= self.averageCalculator(y21)
            else:
                average_Dequeued=self.noZeroAverageCalculator(y21)
            self.draw_one_plot(x21, y21,'r','$Dequeued Difference-AVG:'+str(average_Dequeued)+'$')
        elif self.config['ReportMode']=='E':
            x22,y22=self.setPoint(self.difference_Enqueued)
            if self.config['IsCalZero']=='Z':
                average_Enqueued=self.averageCalculator(y22)
            else:
                average_Enqueued=self.noZeroAverageCalculator(y22)
            self.draw_one_plot(x22, y22,'black','$Enqueued Difference-AVG:'+str(average_Enqueued)+'$')
        else:
            x21,y21=self.setPoint(self.difference_Dequeued)
            x22,y22=self.setPoint(self.difference_Enqueued)
            if self.config['IsCalZero']=='Z':
                average_Enqueued=self.averageCalculator(y22)
                average_Dequeued= self.averageCalculator(y21)
            else:
                average_Dequeued=self.noZeroAverageCalculator(y21)
                average_Enqueued=self.noZeroAverageCalculator(y22)
            self.draw_two_plot(x21, y21,'r','$Dequeued Difference-AVG:'+str(average_Dequeued)+'$',
                       x22,y22,'black','$Enqueued Difference-AVG:'+str(average_Enqueued)+'$')
        #draw the Number Of Consumers
        pl.sca(ax3)
        pl.title('Number Of Consumers')
        pl.ylabel('Number')
        pl.xlabel('Times(1 equals '+self.time+' )')
        x3,y3=self.setPoint(self.Content_NumberOfConsumers[1:])
        self.draw_one_plot(x3, y3,'green','$Consumers$')

        # show the plot on the screen
        pl.show()
    
if __name__ == '__main__':  
    report()
