# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 15:34:33 2019

@author: shiweijun
@E-mail: 824044645@qq.com
"""
import serial
import sys

g_serial = None
def open(name='COM1', baudrate=9600, timeout=3):
    global g_serial
    g_serial = serial.serial_for_url(name, do_not_open=True)
    g_serial.baudrate = baudrate
    g_serial.timeout = timeout
    try:
        g_serial.open()
    except serial.SerialException as e:
        print('Could not open serial port {}: {}\n'.format(g_serial.name, e))
        return False

    return True
    
def write(data):
    g_serial.write(data)
    
def read(size = 1):
    return g_serial.read(size)

def close():
    g_serial.close()
