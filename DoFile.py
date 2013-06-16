# -*- coding: utf-8 -*-
import xml
import os,sys

'''
    They are classes for read file and write file.
    Author:ljchu
    2013/1/18
'''

class ReadFile:
    def __init__(self,filename='',spl='='):
        self.filename=filename
        self.spl=spl
        
    def setFileName(self,filename):
        self.filename=filename

    def ReadTxtBySpl(self):
        Content=[]
        line_no=0
        try:
            with open(self.filename,encoding=sys.getfilesystemencoding())as a_file:
                for a_line in a_file:
#                    print(a_line)
                    if len(a_line) >1 and a_line.find('#') ==-1: 
                        line_no +=1
                        a_Content = a_line.rstrip().split(self.spl)
                        Content.append(a_Content)
                    else:
                        line_no +=1
            #print(Content)
            return(Content)
        except Exception as e:
            #print('Can not read the file: ',e)
            print(e)
            return False
    
class WriteFile:
    def __init__(self,filename=''):
        self.filename=filename
    
    def SetFileName(self,FileName):
        self.filename=FileName
    
    def WriteList(self,a_list):
        try:
            with open(self.filename,mode='a',encoding='utf-8')as a_file:
                a_file.write(str(a_list)+'\n')
        except Exception as e:
            print('Fail to write to the file:',e)
            return 0
