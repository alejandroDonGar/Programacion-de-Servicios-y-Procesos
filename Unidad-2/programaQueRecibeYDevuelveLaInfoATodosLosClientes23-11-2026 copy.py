# 'Chat de clase por terminal'. Todos podemos ver los mensajes de todos y hablar. Se borran los mensajes, solo quedando 1 por cliente ya que no se guardan o registran o concatenan estos.
# Si primero mando un 'hola', y luego 'adios', el 'hola' se borra de la variable.

import socket 

servidor=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

servidor.bind(("",4444))
clientes={} # Diccionario vacio

while True:
    datos,addr = servidor.recvfrom(1024)
    if addr in clientes:
        print("Clientes existentes") # Si la ip o puerto estan en los datos recividos en 'datos,addr = servirod.recvfrom(1024)'
    else:
        print("Cliente nuevo") # Si no, se añade como nuevo
        clientes[addr]=datos 
    for cli in clientes:
        if cli != addr:
            servidor.sendto(f"{addr}: {datos.decode('utf-8')}".encode('utf-8'),cli) # ¿Que hace?