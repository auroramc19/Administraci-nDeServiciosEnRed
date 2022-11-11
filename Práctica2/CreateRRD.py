#!/usr/bin/env python
import rrdtool

def crearRRD(dispositivo):
    ret = rrdtool.create(f"./ArchivoRRD/{dispositivo}.rrd",
                         "--start",'N',
                         "--step",'300',
                         "DS:pUnicastRec:COUNTER:120:U:U",
                         "DS:pRecibidosIP:COUNTER:120:U:U",
                         "DS:mICMPEchoEnv:COUNTER:120:U:U",
                         "DS:segmentosRec:COUNTER:120:U:U",
                         "DS:datagramasUDP:COUNTER:120:U:U",
                         "RRA:AVERAGE:0.5:6:5",
                         "RRA:AVERAGE:0.5:1:1000")

    if ret:
        print (rrdtool.error())