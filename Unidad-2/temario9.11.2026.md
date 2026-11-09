arquitectura cliente-servidor
programas que se pasan informacion a traves de las redes con el tpcip
dos ordenadores

como se identifican cada ordenador en internet?
Con su IP.

para comunicarse con uno necesitamos saber su ip

una vez dentro de la maquina, si queremos ir a un proceso en concreto, habra que buscar si es tcp o udp y su puerto asociado
no se puede salir de tcp e ir a udp. No funcionan igual. TCP numera cada octeto y le pide al otro lado si lo ha recibido, three handshake
udp no lo hace, envia los datos sin importar si sabe si han llegado. 

sniffer y como se conecta con el resto del temario

El puerto de origne y el de destino. Datagrama IP (p.origin, p.destino) Cuando el datagrama ip sale ya sabiendo su ip de origen y puerto. Para hacer un programa tendremos que saber estos puntos de destino. Lo mismo con udp. 

Que pasa con el otro lado del programa? Ese tambien necesita saber mi ip y puerto. Esta informacion la conoce del datagrama ip que se ha enviado desde mi lado con anterioridad. 

| src | dst |    | src | dst|
|---|---|---|---|---|
|ip | ip | tcp | port | port | 
datos <-------

con el primer paquete el segundo ya los sabe los datos de origin

| dst | src |  | dst | src |
|---|---|---|---|---|
| ip | ip | tcp | port | port | 
datos  ------->

en tcp siempre el cliente inicia la conexion y el servidor le responde.

src src  dst dst
ip  port ip  port  <--- socket

que es un socket...

well known ports

si pongo http://ip sin puerto
el navegador automaticamnete interpreta que estas usando http y te manda al puerto 80

si no hay puerto hay que ir al por defecto. El navegador tiene que estar configurado para reconocerlo.

(poner 20 puretos well-known)

Flags [S] , [R], [.], demas
seq
win
options
ecr
nop
ack

ver como es cuando el otro lado tambien responde

(revisar si las explicaciones estan bien y corregirlas)

ejercicio servidor.py(explicar qué hace)

socket.AF_INET -> ipv4
SOCK_STREAM -> tcp
SOCK_DGRAM -> udp

dentro del bind:
"" o "0.0.0.0"-> Cualquier direccion ip que tenga