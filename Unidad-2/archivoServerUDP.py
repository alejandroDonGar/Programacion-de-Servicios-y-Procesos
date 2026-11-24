# Abrir socket, recibir y guarda en un archivo

import socket

servidor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
servidor.bind(("",4444))
# Estas dos lineas van sí o sí siempre. Abrimos y decimos a que ip y puerto

archivo=open('fichero', 'wb')

while True:
    datos,addr = servidor.resvfrom(65536) #Bloqueante
    archivo.write(datos)

    # ¿Como hacemos para que cuando se termine de leer, el server cierre e imprima algo como 'Archivo escrito' o similar?
        