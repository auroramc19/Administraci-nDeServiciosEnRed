import sys
import rrdtool
from  Notify import send_alert_attached
import time
rrdpath = 'RRD/'
imgpath = 'IMG/'

def graficarTrend(archivo_rrd,nom_img,y_label,lw_limit,up_limit,titulo,nom_e,def_e,uMin,uMed,uMax,hostN):
    ultima_lectura = int(rrdtool.last(rrdpath+f"{archivo_rrd}.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 1200

    ret = rrdtool.graphv(imgpath+f"{nom_img}.png",
                         "--start",str(tiempo_inicial),
                         "--end",str(tiempo_final),
                         f"--vertical-label={y_label}",
                        '--lower-limit', f'{lw_limit}',
                        '--upper-limit', f'{up_limit}',
                        f"--title={titulo} \n Detección de umbrales",
                        f"DEF:{nom_e}="+rrdpath+f"{archivo_rrd}.rrd:{def_e}:AVERAGE",
                         f"VDEF:cargaMAX={nom_e},MAXIMUM",
                         f"VDEF:cargaMIN={nom_e},MINIMUM",
                         f"VDEF:cargaSTDEV={nom_e},STDEV",
                         f"VDEF:cargaLAST={nom_e},LAST",
                     #   "CDEF:cargaEscalada=cargaCPU,8,*",
                         f"CDEF:umbralMin={nom_e},{uMin},LT,0,{nom_e},IF",
                         f"CDEF:umbralMed={nom_e},{uMed},LT,0,{nom_e},IF",
                         f"CDEF:umbralMax={nom_e},{uMax},LT,0,{nom_e},IF",
                         #f"AREA:{nom_e}#00FF00:{titulo}",
                         f"AREA:umbralMin#00FF00:{titulo} mayor que {uMin}",
                         f"AREA:umbralMed#FFA500:{titulo} mayor que {uMed}",
                         f"AREA:umbralMax#FF4500:{titulo} mayor que {uMax}",
                         f"HRULE:{uMin}#0000FF:Umbral {uMin} - {uMed}%",
                         f"HRULE:{uMed}#FFFF00:Umbral {uMed} - {uMax}%",
                         f"HRULE:{uMax}#FF0000:Umbral {uMax} - 100%",
                         "PRINT:cargaLAST:%6.2lf",
                         "GPRINT:cargaMIN:%6.2lf %SMIN",
                         "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                         "GPRINT:cargaLAST:%6.2lf %SLAST" )
    #print (ret)

    ultimo_valor=float(ret['print[0]'])
    if ultimo_valor > uMax:
        send_alert_attached("Sobrepasa Umbral Ready",f"{nom_img}.png",hostN,titulo)
        print("Sobrepasa Umbral Ready")
        exit()
    #if ultimo_valor > uMed:
    #    send_alert_attached("Sobrepasa Umbral Set",f"{nom_img}.png",hostN,titulo)
    #    print("Sobrepasa Umbral Set")
    #    exit()
    #if ultimo_valor > uMin:
    #   send_alert_attached("Sobrepasa Umbral Go",f"{nom_img}.png",hostN,titulo)
    #   print("Sobrepasa Umbral Go")
    #   exit()