import sys
import rrdtool
import time

def graphCreate(nom_elemento,def_elemento,archivo_rrd,y_label,tituloG,color,tipo):
    tiempo_actual = int(time.time())
    #Grafica desde el tiempo actual menos diez minutos
    tiempo_inicial = (tiempo_actual) - 86500

    ret = rrdtool.graphv( f"./GraficasRRD/{nom_elemento}.png",
                         "--start",str(tiempo_inicial),
                         "--end","N",
                         f"--vertical-label={y_label}",
                         f"--title={tituloG}",
                         f"DEF:{nom_elemento}={archivo_rrd}.rrd:{def_elemento}:AVERAGE",
                         f"CDEF:escalaIn={nom_elemento},8,*",
                         f"AREA:escalaIn{color}:{tipo}",
                          )
    print(ret)