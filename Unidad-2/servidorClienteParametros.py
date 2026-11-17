import socket,sys

cliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente.connect((sys.argv[1],int(sys.argv[2]))) # Explicar la diferencia entre esto y la forma anterior de servidorCliente.py sin parametros
# Aqui el cliente puede especificar a que IP y Puerto conectarse.

a=input("Qué enviamos?")
cliente.sendall(a.encode('utf-8'))

respuesta=cliente.rec(1024)
print(respuesta.decode('utf-8'))
cliente.close() # <- Encia el sinq y ack el solo
