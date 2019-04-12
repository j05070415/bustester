# -*- coding: utf-8 -*-
"""
Created on Tue Apr 09 15:10:22 2019

@author: shiweijun
@E-mail: 824044645@qq.com
"""
from ctypes import *
import binascii
import re
import struct

class TagHeader(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
            ('flag', c_ubyte),
            ('res', c_ubyte),
            ('len', c_ushort),
            ('net', c_ubyte),
            ('time', c_ubyte*3),
            ('ifg', c_ubyte),
            ('res1', c_ubyte*7)
            ]
    
class TagHeader4x(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
            ('port_flag', c_uint),
            ('invalid_len', c_ubyte),
            ('flag', c_ubyte),
            ('net', c_ubyte),
            ('res', c_ubyte),
            ('len', c_ushort),
            ('frag_len', c_ushort),
            ('res1', c_ushort),
            ('ip_header', c_ushort),
            ('src_port', c_ushort),
            ('dst_port', c_ushort),
            ('dst_vl', c_ushort),
            ('user_define_id', c_ushort),
            ('src_ip', c_uint),
            ('dst_ip', c_uint),
            ('res2', c_ubyte*16),
            ('ifg', c_ubyte),
            ('time', c_ubyte*3)
            ]
    
class PreambleHeader(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
            ('preamble', c_ubyte*7),
            ('start_delimiter', c_ubyte)
            ]

class _DMAC(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
            ('d_field', c_uint),
            ('vl', c_ushort)
            ]
    
class _SMAC(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
            ('s_field', c_ubyte*3),
            ('user_id', c_ushort),
            ('net', c_ubyte, 3),
            ('field1', c_ubyte, 5)
            ]
    
class _EType(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
            ('eh_type', c_ushort)
            ]
    
class MACHDR(Structure):
    _pack_ = 1
    _anonymous_ = ('dmac', 'smac', '_type')
    _fields_ = [
            ('dmac', _DMAC),
            ('smac', _SMAC),
            ('_type', _EType)
            ]
    
class IP4HDR(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
            ('ih_ver', c_ubyte, 4),
            ('ih_ihl', c_ubyte, 4),
            ('ih_tos', c_ubyte),
            ('ih_len', c_ushort),
            ('ih_id', c_ushort),
            ('ih_fragment', c_ushort),
            ('ih_ttl', c_ubyte),
            ('ih_protocol', c_ubyte),
            ('ih_checksum', c_ushort),
            ('ih_src', c_uint),
            ('ih_dst', c_uint)
            ]
    
class UDPHDR(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
            ('uh_src', c_ushort),
            ('uh_dst', c_ushort),
            ('uh_len', c_ushort),
            ('uh_checksum', c_ushort)
            ]
    
class FrameHeader(Structure):
    _pack_ = 1
    _anonymous_ = ('pre', 'mac', 'ip', 'udp')
    _fields_ = [
            ('pre', PreambleHeader),
            ('mac', MACHDR),
            ('ip', IP4HDR),
            ('udp', UDPHDR)
            ]

class Packet(Structure):
    _pack_ = 1
    _anonymous_ = ('tag', 'frame')
    _fields_ = [
            ('tag', TagHeader),
            ('frame', FrameHeader)
            ]

class Packet4x(Structure):
    _pack_ = 1
    _anonymous_ = ('tag', 'frame')
    _fields_ = [
            ('tag', TagHeader4x),
            ('frame', FrameHeader)
            ]
    
def MACToString(mac):
    decoded = binascii.hexlify(mac).decode('ascii')
    formatted = re.sub(r'(.{2})(?!$)', r'\1:', decoded)
    return formatted

def MACFromString(mac):
    mac = mac.replace(":", "")
    return binascii.unhexlify(mac)
    
def parseTagTime(t):
    value = 0
    value |= t[0] << 16
    value |= t[1] << 8
    value |= t[2]
    
    return value/1000

def modifyTagTime(data, value):
    value *= 1000
    src = struct.pack(">I", value)
    memmove(data, src[1:], 3)
    
def unpack(data):
    if len(data) < sizeof(Packet): return
    packet = Packet()
    memmove(byref(packet), data, sizeof(packet))
    
    return packet

def unpack4(data):
    if len(data) < sizeof(Packet4x): return
    packet = Packet4x()
    memmove(byref(packet), data, sizeof(packet))
    
    return packet

if __name__ == "__main__":
    macstr = MACToString(b'\x01\x02\x03\x04\x05\x06')
    print "expect:01:02:03:04:05:06=", macstr
    print repr(MACFromString(macstr))
    raw = binascii.unhexlify("14000067030003e8000000000000000055555555555556d503000000000102000003046008004500004c00000000011164dd0a0000010a000102030405060038e0f8ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00d0cb83c100")
    raw4x = binascii.unhexlify("000000000906030000630000000000000000000000000000000000000000000000000000000000000000000000000000000003e855555555555553d503000000000502000001026008004500004c00000000011164be0a0000010a000102030405060038df08ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000")
    Tag = TagHeader()
    Tag4x = TagHeader4x()
    frame = FrameHeader()
    frame4x = FrameHeader()
    print 'expect:16 52 50=', sizeof(Tag), sizeof(Tag4x), sizeof(frame)
    print 'expect:8 14 20 8=', sizeof(PreambleHeader), sizeof(MACHDR), sizeof(IP4HDR), sizeof(UDPHDR)

    print 'raw size:', len(raw)
    print 'raw4x size:', len(raw4x)
    memmove(byref(Tag), raw, sizeof(Tag))
    memmove(byref(Tag4x), raw4x, sizeof(Tag4x))
    memmove(byref(frame), raw[sizeof(Tag):], sizeof(frame))
    memmove(byref(frame4x), raw4x[sizeof(Tag4x):], sizeof(frame4x))
    print "tag expect:20 103 3 0=", Tag.flag, Tag.len, Tag.net, Tag.ifg, binascii.hexlify(Tag.time)
    print "expect:1 = ", parseTagTime(Tag.time)
    print "4x tag expert:9 6 3 99 0 0003e8=", Tag4x.invalid_len, Tag4x.flag, Tag4x.net, Tag4x.len, Tag4x.ifg, binascii.hexlify(Tag4x.time)
    print "4x time expect:1 = ", parseTagTime(Tag4x.time)
    
    print "expect:0003e8=", binascii.hexlify(Tag.time)
    modifyTagTime(Tag.time, 2)
    print "expect:0007d0=", binascii.hexlify(Tag.time)
    
    print "4x time expect:0003e8=", binascii.hexlify(Tag4x.time)
    modifyTagTime(Tag4x.time, 3)
    print "4x time expect:000bb8=", binascii.hexlify(Tag4x.time)
    print "pre expect:55555555555556 d5=", binascii.hexlify(frame.preamble), binascii.hexlify(struct.pack("B", frame.start_delimiter))
    print "4x pre expect:55555555555553 d5=", binascii.hexlify(frame4x.preamble), binascii.hexlify(struct.pack("B", frame4x.start_delimiter))
    
    print 'mac expect:03000000 0001=', binascii.hexlify(struct.pack(">I",frame.d_field)), binascii.hexlify(struct.pack(">H",frame.vl))
    print '4x mac expect:03000000 0005=', binascii.hexlify(struct.pack(">I",frame4x.d_field)), binascii.hexlify(struct.pack(">H",frame4x.vl))
    print 'mac expect:020000 0304 3=', binascii.hexlify(frame.s_field), binascii.hexlify(struct.pack(">H",frame.user_id)), frame.net
    print '4x mac expect:020000 0102 3 0800=', binascii.hexlify(frame4x.s_field), binascii.hexlify(struct.pack(">H",frame4x.user_id)), frame4x.net, binascii.hexlify(struct.pack(">H",frame4x.eh_type))
    
    print 'ip expect: 4 5 004c 1 17 64dd 0a000001 0a000102=', frame.ih_ver, frame.ih_ihl, binascii.hexlify(struct.pack(">H", frame.ih_len)), frame.ih_ttl, frame.ih_protocol, binascii.hexlify(struct.pack(">H", frame.ih_checksum)), binascii.hexlify(struct.pack(">I", frame.ih_src)), binascii.hexlify(struct.pack(">I", frame.ih_dst))    
    print '4x ip expect: 4 5 004c 1 17 64be 0a000001 0a000102=', frame4x.ih_ver, frame4x.ih_ihl, binascii.hexlify(struct.pack(">H", frame4x.ih_len)), frame4x.ih_ttl, frame4x.ih_protocol, binascii.hexlify(struct.pack(">H", frame4x.ih_checksum)), binascii.hexlify(struct.pack(">I", frame4x.ih_src)), binascii.hexlify(struct.pack(">I", frame4x.ih_dst))
    
    print 'udp expect:0304 0506 0038 e0f8=', binascii.hexlify(struct.pack(">H",frame.uh_src)), binascii.hexlify(struct.pack(">H",frame.uh_dst)), binascii.hexlify(struct.pack(">H",frame.uh_len)), binascii.hexlify(struct.pack(">H",frame.uh_checksum))
    print '4x udp expect:0304 0506 0038 df08=', binascii.hexlify(struct.pack(">H",frame4x.uh_src)), binascii.hexlify(struct.pack(">H",frame4x.uh_dst)), binascii.hexlify(struct.pack(">H",frame4x.uh_len)), binascii.hexlify(struct.pack(">H",frame4x.uh_checksum))
    
    print 'expect:66 102={} {}'.format(sizeof(Packet), sizeof(Packet4x))
    pack1 = unpack(raw)
    pack2 = unpack4(raw4x)
    print pack1.tag.flag, pack1.tag.len, pack1.tag.net, pack1.frame.vl, pack1.frame.ih_ver
    print pack2.tag.invalid_len,  pack2.tag.flag, pack2.tag.len, pack2.tag.net, pack2.frame.vl, pack2.frame.ih_ver
    
    
    

    
