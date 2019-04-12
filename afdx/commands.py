# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 15:10:22 2019

@author: shiweijun
@E-mail: 824044645@qq.com
"""
from ctypes import *

##Command Type
NULLCommand = 0x00
Configure = 0x10
ConfigComplete = 0x11
ComWrite = 0x20
SapWrite = 0x21
ComRead = 0x30
ComReadResp = 0x31
SapRead = 0x40
SapReadResp = 0x41
TestOF = 0x50
TestOFResponse = 0x51
RxControl = 0x60
MultiComWrite = 0x70
CreatePort = 0x80
CreatePortResp = 0x81
SendIcmpCommand = 0x90
ReadIcmpCommand = 0x91
Acknowlege = 0xF1
Reset = 0xFE
Error = 0xE1

##Configure Type
ConfigBegin = 0x01,
ConfigSNIC = 0x02,
ConfigTxNIOS = 0x03,
ConfigRxNIOS = 0x04,
ApplyConfig = 0x05

##Rx Port Type
COM_UDP = 0
SAP_IP = 1
SAP_UDP = 2
SAP_MAC = 3

class ICMPHeader(Structure):
    _fields_ = [
            ('type', c_ubyte),
            ('code', c_ubyte),
            ('checksum', c_ushort),
            ('identifier', c_ushort),
            ('sequence', c_ushort),
            ]

class SendIcmp(Structure):
    _fields_ = [            
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('port_id', c_ushort),
            ('perchar', c_ubyte),
            ('reserve2', c_ubyte),
            ('ipdst', c_uint),
            ('size', c_uint),
            ('repeat', c_uint),
            ]

class ReadIcmp(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('reserve1', c_ubyte),
            ('reserve2', c_ubyte),
            ('port_id', c_uint),
            ]

##UDPSeq,ConfigureComplete
class CommandMessage(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('reserved1', c_ubyte),
            ('reserved2', c_ubyte),
            ]

class CreatePortCommand(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('reserved1', c_ubyte),
            ('reserved2', c_ubyte),
            ('direction', c_uint),
            ('vl', c_uint),
            ('ipsrc', c_uint),
            ('ipdst', c_uint),
            ('udpsrc', c_uint),
            ('udpdst', c_uint),
            ]

class CreatePortResponse(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('result', c_uint),
            ]

class ConfigureCommand(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('reserved1', c_ubyte),
            ('reserved2', c_ubyte),
            ('protocol', c_uint),
            ('caseid', c_uint),
            ('configname', c_char*32),
            ]

class ComReadCommand(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('port', c_uint),
            ]

class TimeStamp(Structure):
    _fields_ = [  
            ('mDay', c_uint),
            ('mHour', c_uint),
            ('mMinute', c_uint),
            ('mSecond', c_uint),
            ('mNanosecond', c_uint),
            ]

class ComReadResponsePayload(Structure):
    _fields_ = [  
            ('message_size', c_uint),
            ('network', c_uint),
            ('fresh', c_uint),
            ('fsn', c_uint),
            ('time', TimeStamp),
            ]

class ComReadResponse(Structure):
    _anonymous_ = ('payload',)
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('chunk_count', c_ubyte),
            ('chunk_index', c_ubyte),
            ('cnt', c_ushort),
            ('payload', ComReadResponsePayload),
            ]

class WriteData(Structure):
    _fields_ = [  
            ('write_type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('r3', c_ubyte),
            ('repeat_count', c_uint),
            ('message_size', c_uint),
            ]

class ComWriteCommand(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('port_ID', c_uint),
            ('tx_repeat', c_uint),
            ('tx_data_count', c_uint),
            ]

class MultiComWriteCommand(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('tx_repeat', c_uint),
            ('message_size', c_uint),
            ('perchar', c_ubyte),
            ('r3', c_ubyte),
            ('r4', c_ubyte),
            ('r5', c_ubyte),
            ('port_Count', c_uint),
            ]

class SapReadCommand(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('port', c_uint),
            ]

class SapReadResponsePayload(Structure):
    _fields_ = [  
            ('message_size', c_uint),
            ('ip_addr', c_uint),
            ('udp_addr', c_uint),
            ('network', c_uint),
            ('time', TimeStamp),
            ]

class SapReadResponse(Structure):
    _anonymous_ = ('payload',)
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('chunk_count', c_ubyte),
            ('chunk_index', c_ubyte),
            ('cnt', c_ushort),
            ('payload', SapReadResponsePayload),
            ]

class SapWriteCommand(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('port_id', c_uint),
            ('dest_ip', c_uint),
            ('dest_udp', c_ushort),
            ('r3', c_ubyte),
            ('r4', c_ubyte),
            ('repeat_count', c_uint),
            ('tx_data_count', c_uint),
            ]

class TestOverflowCommand(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('port_type', c_uint),
            ('port', c_uint),
            ]

class TestOverflowResponse(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('is', c_uint),
            ]

class ResetCommand(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ]

class Acknowledge(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('received_platform', c_ubyte),
            ('received_type', c_ubyte),
            ('r3', c_ubyte),
            ('r4', c_ubyte),
            ]

class ErrorMessage(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('error', c_uint),
            ('message_size', c_uint),
            ]

class RxPortControlCommand(Structure):
    _fields_ = [  
            ('platform', c_ubyte),
            ('type', c_ubyte),
            ('port_id', c_ushort),
            ('port_type', c_uint),
            ('opened', c_ubyte),
            ('r1', c_ubyte),
            ('r2', c_ubyte),
            ('r3', c_ubyte),
            ]