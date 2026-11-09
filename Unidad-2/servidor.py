import socket
#AF_INET -> IPv4
#DGRAM -> udp
#STREAM -> tcp
servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

servidor.bind(("",4444))
servidor.listen()

a=input("aquí esperando")
