import socket

# Socket de escuha en IPv4(socket.AF_INET) + TCP(socket.SOCK_STREAM)
servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Configura donde escuchar. En todas las IPs que tenga y en el puerto 4444
servidor.bind(("0.0.0.0", 4444))
# Ahora ya si esta escuchando
servidor.listen()
input("Aquí esperando")

# AlejandroDonate@debian-des:~/Escritorio/Programacion-de-Servicios-y-Procesos/Unidad-2$ ss -putnl
# Netid   State    Recv-Q   Send-Q     Local Address:Port      Peer Address:Port  Process                                                                         
# udp     UNCONN   0        0                0.0.0.0:5353           0.0.0.0:*                                                                                     
# udp     UNCONN   0        0                0.0.0.0:56795          0.0.0.0:*                                                                                     
# udp     UNCONN   0        0                   [::]:54434             [::]:*                                                                                     
# udp     UNCONN   0        0                   [::]:5353              [::]:*                                                                                     
# tcp     LISTEN   0        128              0.0.0.0:4444           0.0.0.0:*      users:(("python3",pid=25805,fd=3))                                             
# tcp     LISTEN   0        200            127.0.0.1:5432           0.0.0.0:*                                                                                     
# tcp     LISTEN   0        4096             0.0.0.0:8069           0.0.0.0:*                                                                                     
# tcp     LISTEN   0        128              0.0.0.0:22             0.0.0.0:*                                                                                     
# tcp     LISTEN   0        4096           127.0.0.1:631            0.0.0.0:*                                                                                     
# tcp     LISTEN   0        4096             0.0.0.0:2222           0.0.0.0:*                                                                                     
# tcp     LISTEN   0        4096             0.0.0.0:3000           0.0.0.0:*                                                                                     
# tcp     LISTEN   0        4096               [::1]:631               [::]:*                                                                                     
# tcp     LISTEN   0        4096                [::]:8069              [::]:*                                                                                     
# tcp     LISTEN   0        128                 [::]:22                [::]:*                                                                                     
# tcp     LISTEN   0        200                [::1]:5432              [::]:*                                                                                     
# tcp     LISTEN   0        4096                [::]:2222              [::]:*                                                                                     
# tcp     LISTEN   0        4096                [::]:3000              [::]:*  