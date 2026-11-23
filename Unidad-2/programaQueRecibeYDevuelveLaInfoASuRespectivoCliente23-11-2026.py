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
    print(f"{addr}: {datos.decode('utf-8')}")
    servidor.sendto(f"Echo: {datos.decode('utf-8')}".encode('utf-8'),addr)