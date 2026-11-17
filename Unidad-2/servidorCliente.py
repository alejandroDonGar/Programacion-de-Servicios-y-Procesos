import socket
# Explicar este codigo y como se relaciona con el temario e incorporar los conocimeintos al temarios de la unidad

cliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente.connect(("10.108.255.0",4444)) # No se hace "" porque el cliente tiene que saber a donde conectarse

