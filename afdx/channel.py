# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 16:01:04 2019

@author: shiweijun
@E-mail: 824044645@qq.com
"""
import PyStorage as ps
import PyAdapter as pa

class Channel:
    def __init__(self, key):
        self.key = key
        
    def read(self, index, count):
        return ps.data(self.key, index, count)
    
    def write(self, data):
        ps.send(self.key, data)