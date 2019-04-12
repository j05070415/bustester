# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 16:05:19 2019

@author: shiweijun
@E-mail: 824044645@qq.com
"""
import PyAdapter as pa

class AFDXCard1000MNormal(AFDXCard):
    def __init__(self, id):
        super(AFDXCard, self).__init__(id)
        self.adaptername = "AFDXAdapter"
        self.halname = "AFDX4Normal_Hwa"
        if not pa.initAdapter(self.adaptername, self.halname):
            print('AFDXCard1000MNormal init adapter failed!')
        
    def open(self, config):
        return pa.open(self.adaptername, self.halname, config)
    
    def close(self):
        return pa.close(self.adaptername)
    
    def __exit__(self):
        self.close()