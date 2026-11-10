import socket
#AF_INET -> IPv4
#DGRAM -> udp
#STREAM -> tcp
servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

servidor.bind(("",4444))
servidor.listen()
socket_cliente,addre=servidor.accept()

print(f"IP_Cliente= {addr[0]} Puerto_Cliente= {addr[1]} Protocolo= TCP")
datos=socket_cliente.recv(1024) #LINEA BLOQUEANTE
print(datos.decode('utf-8')) # .decode('utf-9') Hace que los datos binario se decodifique y se puestren como letras
socket_cliente.sendall("Mensaje recibido".encode('utf-8')) # Hace lo mismo pero al reves, coge los datos en alfabeto y los transforma en binario para enviarlos en la respuesta a la maquina de origen
socket_cliente.close() # Como ya no se queda esperando, lo cerramos para este cliente. (Le livera la terminal al alumno en su pc ya que antes aunque legar la info se le queadba la terminal bloqueda en mabos pcs auqnue ya se estuviera leyendo el segundo)
a=input("aquí esperando")

socket_cliente,addre=servidor.accept()
print(f"IP_Cliente= {addr[0]} Puerto_Cliente= {addr[1]} Protocolo= TCP")


