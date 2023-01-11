import ftplib
import telnetlib

def generarArchivoConfig(host, user, pwd):
    comando = "copy run start"
    ftp = "service ftp"
    try:
        tn = telnetlib.Telnet(host)
        print('conectado\n')
        tn.read_until(b"User: ")
        tn.write(user.encode('ascii') + b"\n")
        if pwd:
            tn.read_until(b"Password: ")
            tn.write(pwd.encode('ascii') + b"\n")

        tn.write(b"enable\n")
        tn.write(b"config\n")
        tn.write(ftp.encode('ascii') + b"\n")
        tn.write(comando.encode('ascii') + b"\n")
        tn.write(b"exit\n")
        tn.write(b"exit\n")

        print("Archivo generado\n")
        aux = tn.read_all()
        #print(aux)

    except Exception as ex:
        print('\nSe produjo un error al generar el archivo de configuración')
        print(ex+'\n')

def extraerArchivoConfig(host, user, pwd, nomA:str=''):
    try:
        ftp = ftplib.FTP(host)
        ftp.login(user, pwd)
        
        archivo = ''
        if nomA != '':
            archivo = nomA
        else:
            archivo = 'startup-config_' + host.replace('.', '_')
        print(archivo)
        ftp.retrbinary('RETR startup-config', open('./ArchivosConfig/' + archivo, 'wb').write)
        print("Archivo recibido y guardado en /ArchivosConfig\n")

        ftp.quit()

    except Exception as ex:
        print('\nSe produjo un error al extraer el archivo de configuración')
        print(ex+'\n')

def enviarArchivoConfig(host, user, pwd, nomA:str=''):
    try:

        ftp = ftplib.FTP(host)
        ftp.login(user, pwd)

        ubicacion = './ArchivosConfig/'
        if nomA != '':
            ubicacion += nomA
        else:
            ubicacion += 'startup-config_' + host.replace('.', '_')

        archivo = open(ubicacion, 'rb')
        #print(archivo.readlines())

        ftp.storbinary('STOR startup-config', archivo)
        print("Archivo enviado") 

        ftp.quit()

    except Exception as ex:
        print('\nSe produjo un error al enviar el archivo de configuración')
        print(ex+'\n')

    