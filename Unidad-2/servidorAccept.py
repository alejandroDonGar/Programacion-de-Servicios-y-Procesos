import socket
#AF_INET -> IPv4
#DGRAM -> udp
#STREAM -> tcp
servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

servidor.bind(("",4444))
servidor.listen()
socket_cliente,addre=servidor.accept()

print(f"IP_Cliente= {addr[0]} Puerto_Cliente= {addr[1]} Protocolo= TCP}}")
a=input("aquí esperando")
