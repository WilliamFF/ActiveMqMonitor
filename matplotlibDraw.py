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
        configFile=self.getFatherPath(os.getcwd())+'config.txt'
        if os.path.exists(configFile)!=1:
            print('[WARN]Can not find the config file: '+configFile)
            return
        readFile = ReadFile()
        readFile.setFileName(configFile)
        self.config=dict(readFile.ReadTxtBySpl())
        self.file=self.config['MonitorFileName']
        if os.path.exists(self.file)!=1:
            print('[WARN]Can not find the monitor file: '+self.file)
            return
        
        self.time=self.config['IntervalTime']
        self.fontSize=10
        
        self.Content_MessagesDequeued=[]
        self.Content_NumberOfPendingMessages=[]
        self.Content_NumberOfConsumers=[]
        self.Content_MessagesEnqueued=[]
        self.difference_Dequeued=[]
        self.difference_Enqueued=[]
        
        self.getMessageList()
        self.creatReport()
    
    def getFatherPath(self,c_path):
        b=c_path.split('\\')
        f_path=''
        for i in range(0,len(b)-1):
            c=b[i]+'\\'
            f_path+=c
        return f_path
    
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
        t=0
        for i in a_list:
            t+=int(i)
        a=t/len(a_list)
        b="%.2f" %a
        return b

    def getMessageList(self):
        line_no=0
        try:
            with open(self.file,encoding=sys.getfilesystemencoding())as a_file:
                for a_line in a_file:
                    line_no +=1
                    a_Content = a_line.rstrip().split('\t')
                    if a_Content[4].find('MessagesDequeued')==-1:
                        self.Content_NumberOfPendingMessages.append(a_Content[1])
                        self.Content_NumberOfConsumers.append(a_Content[2])
                        self.Content_MessagesEnqueued.append(a_Content[3])
                        self.Content_MessagesDequeued.append(a_Content[4])
                    else:
                        line_no +=1
        except Exception as e:
            print(e)
            return

        for j in range(1,len(self.Content_MessagesDequeued)):
            self.difference_Dequeued.append(int(self.Content_MessagesDequeued[j])-int(self.Content_MessagesDequeued[j-1]))
            self.difference_Enqueued.append(int(self.Content_MessagesEnqueued[j])-int(self.Content_MessagesEnqueued[j-1]))
            
    
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
            
    def creatReport(self):
        pl.figure(1)
        ax1 = pl.subplot(311)
        ax2 = pl.subplot(312)
        ax3 = pl.subplot(313)
    
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
    
        pl.sca(ax2)
        pl.title('Messages Difference (per '+self.time+' seconds)')
        pl.ylabel('Number')
        if self.config['ReportMode']=='D':
            x21,y21=self.setPoint(self.difference_Dequeued)
            average_Dequeued= self.averageCalculator(y21)
            self.draw_one_plot(x21, y21,'r','$Dequeued Difference-AVG:'+str(average_Dequeued)+'$')
        elif self.config['ReportMode']=='E':
            x22,y22=self.setPoint(self.difference_Enqueued)
            average_Enqueued=self.averageCalculator(y22)
            self.draw_one_plot(x22, y22,'black','$Enqueued Difference-AVG:'+str(average_Enqueued)+'$')
        else:
            x21,y21=self.setPoint(self.difference_Dequeued)
            x22,y22=self.setPoint(self.difference_Enqueued)
            average_Enqueued=self.averageCalculator(y22)
            average_Dequeued=self.averageCalculator(y21)
            self.draw_two_plot(x21, y21,'r','$Dequeued Difference-AVG:'+str(average_Dequeued)+'$',
                       x22,y22,'black','$Enqueued Difference-AVG:'+str(average_Enqueued)+'$')
    
        pl.sca(ax3)
        pl.title('Number Of Consumers')
        pl.ylabel('Number')
        pl.xlabel('Times(1 equals '+self.time+' seconds)')
        x3,y3=self.setPoint(self.Content_NumberOfConsumers[1:])
        self.draw_one_plot(x3, y3,'green','$Consumers$')

        # show the plot on the screen
        pl.show()
    
if __name__ == '__main__':  
#    main()
    report()
