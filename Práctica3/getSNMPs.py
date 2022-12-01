from pysnmp.hlapi import *

def consultaSNMP(comunidad,host,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        return varBinds[0][1]
    #    for varBind in varBinds:
    #        varB=(' = '.join([x.prettyPrint() for x in varBind]))
    #        resultado= varB.split()[2]
    # return resultado

print(consultaSNMP('AuroraMendez','192.168.1.68','1.3.6.1.2.1.25.2.3.1.3.4'))
#identificarRAM('comunidadASRLub', '192.168.1.64')