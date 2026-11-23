# ¿Qué ocurre en este programa?

import socket,sys

ip_server = sys.argv[1] # Recibe el puerto como int por defecto. ¿De donde la recibe?
port_server = int(sys.argv[2]) # Recibe el piuerto como string y lo trasformamos a int. ¿De donde lo recibe?

cliente = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

servidor = (ip_server,port_server) # Tupla = lista no modificable
cliente.connect(servidor)

while True:
    mensaje=input("Mensaje para enviar: ")
    cliente.sendto(mensaje.encode('utf-8'),servidor)
    respuesta,addr = cliente.recvfrom(1024)
    print(respuesta.decode('utf-8'))