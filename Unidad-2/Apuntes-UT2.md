# UT2 · Comunicación en red: sockets

Apuntes de Programación de Servicios y Procesos (2º DAM 2026-2027), a partir de las notas de clase del 26/10, el 05/11, el 09/11 y el 10/11/2026.

> 📚 Libro de referencia: *Programación de Servicios y Procesos en Python*. Cuando el profesor suba el temario de la UT2 al Campus, se completan estos apuntes con él.

> ✏️ Los bloques marcados como **Corrección** arreglan algo que quedó mal apuntado en clase. Los de **Ampliación** añaden algo que no se dio pero ayuda a entenderlo.

---

## 1. Arquitectura cliente-servidor

En esta unidad los programas ya no se quedan en un solo ordenador: **dos programas en dos máquinas distintas se pasan información por la red usando TCP/IP**.

- El **servidor** se queda esperando (escuchando) en un puerto conocido.
- El **cliente** es el que **inicia** la comunicación con el servidor.

```
   Cliente (192.168.1.10)                     Servidor (192.168.1.20)
  ┌──────────────────────┐    petición    ┌──────────────────────┐
  │ navegador, nc,       │ ─────────────> │ programa escuchando  │
  │ programa Python...   │ <───────────── │ en el puerto 4444    │
  └──────────────────────┘   respuesta    └──────────────────────┘
```

Enlace con la UT1: un servidor web es exactamente esto. El programa principal escucha en el puerto TCP 80 y lanza **un hilo por cada petición** (ver `Unidad-1/Apuntes-UT1.md`, apartado 7).

---

## 2. Cómo se llega a un proceso concreto de otra máquina

Hacen falta tres datos:

| Paso | Dato | Para qué |
|---|---|---|
| 1 | **Dirección IP** | Identifica al **ordenador** en la red. Sin saber su IP no podemos hablar con él. |
| 2 | **Protocolo de transporte**: TCP o UDP | Dentro de la máquina, cada protocolo tiene **sus propios puertos**. |
| 3 | **Puerto** (0-65535) | Identifica al **proceso** que escucha dentro de esa máquina. |

> ➕ **Ampliación:** el puerto TCP 53 y el puerto UDP 53 son **dos puertos distintos**. Es lo que en clase se dijo como «no se puede salir de TCP e ir a UDP»: un paquete TCP nunca llega a un programa que escucha en UDP, aunque el número de puerto sea el mismo. Funcionan de forma distinta y el sistema operativo los lleva por separado.

### TCP frente a UDP

| | **TCP** (`SOCK_STREAM`) | **UDP** (`SOCK_DGRAM`) |
|---|---|---|
| Conexión | Sí. Antes de enviar datos se establece con el *three-way handshake* | No. Se envía directamente |
| Fiabilidad | **Numera cada octeto** (número de secuencia) y el otro lado confirma lo recibido (ACK). Lo que no se confirma se reenvía | Envía los datos **sin saber si han llegado** |
| Orden | Entrega los datos en orden | Pueden llegar desordenados o no llegar |
| Uso típico | Web (HTTP/HTTPS), SSH, correo, bases de datos | DNS, streaming, juegos, VoIP |

> ✏️ **Corrección:** en las notas aparece «TCP numera cada octeto y le pide al otro lado si lo ha recibido, *three handshake*». Son dos cosas distintas:
>
> - El ***three-way handshake*** (saludo en tres pasos: `SYN` → `SYN-ACK` → `ACK`) solo se hace **una vez, al abrir la conexión**.
> - La **confirmación de los datos** se hace durante toda la conexión con el número de secuencia (`seq`) y el de confirmación (`ack`).

### El *three-way handshake*

```
  Cliente                                   Servidor (escuchando)
     │ ── SYN      seq=x ────────────────────────> │   1. «Quiero conectar»
     │ <─ SYN-ACK  seq=y, ack=x+1 ──────────────── │   2. «Vale, yo también»
     │ ── ACK      ack=y+1 ──────────────────────> │   3. «Recibido»
     │ ═════════ conexión establecida ═════════════ │
```

**En TCP siempre es el cliente el que inicia la conexión** y el servidor le responde.

---

## 3. Origen y destino: los dos lados de la comunicación

Cada paquete lleva **IP y puerto de origen** y **IP y puerto de destino**.

Cuando el cliente envía el primer paquete, ya sabe su IP y su puerto de origen (el puerto lo elige el sistema operativo al azar) y tiene que conocer la IP y el puerto del servidor:

| IP origen | IP destino | | Puerto origen | Puerto destino |
|---|---|---|---|---|
| IP del cliente | IP del servidor | TCP | puerto del cliente (aleatorio) | 4444 |

El servidor **no necesita saber nada de antemano** del cliente: lo lee del primer paquete que le llega. Para responder, **intercambia origen y destino**:

| IP origen | IP destino | | Puerto origen | Puerto destino |
|---|---|---|---|---|
| IP del servidor | IP del cliente | TCP | 4444 | puerto del cliente |

> ✏️ **Corrección:** en las notas aparece «Datagrama IP (p. origen, p. destino)». La cabecera IP solo lleva las **direcciones IP**. Los **puertos** van en la cabecera de **TCP** (segmento) o de **UDP** (datagrama), y esa cabecera viaja **dentro** del paquete IP (encapsulación):
>
> ```
> ┌───────────────────────── paquete IP ─────────────────────────┐
> │ cabecera IP: IP origen, IP destino │ ┌──── segmento TCP ────┐ │
> │                                    │ │ puertos, seq, ack,   │ │
> │                                    │ │ flags │ datos        │ │
> │                                    │ └──────────────────────┘ │
> └──────────────────────────────────────────────────────────────┘
> ```

---

## 4. Qué es un socket

Un **socket** es el punto de comunicación que el sistema operativo da a un programa para enviar y recibir datos por la red. Para el programa es como un fichero en el que se escribe y del que se lee.

| Tipo | Se identifica por | Ejemplo |
|---|---|---|
| **Socket de escucha** (servidor esperando) | `[ip, puerto]` local | `0.0.0.0:4444` |
| **Socket de conexión** (una conexión ya establecida) | `[ip_origen, puerto_origen, ip_destino, puerto_destino]` | `192.168.1.10:51234 ↔ 192.168.1.20:4444` |

> ➕ **Ampliación:** como cada conexión se distingue por los **cuatro** datos, un servidor puede tener a la vez miles de conexiones en el **mismo puerto 4444**: cambia la IP o el puerto del cliente. Por eso un servidor web atiende a muchos navegadores en el puerto 80 (un socket de conexión, y normalmente un hilo, por cada uno).

---

## 5. Puertos bien conocidos (*well-known ports*)

Los puertos **0-1023** están reservados para servicios estándar. Si escribimos `http://ip` sin puerto, el navegador sabe que es HTTP y va **al puerto por defecto, el 80** (con `https://`, al 443). Si el servicio está en otro puerto, hay que escribirlo: `http://ip:8069`.

| Puerto | Protocolo | Servicio |
|---|---|---|
| 20 / 21 | TCP | FTP (datos / control) |
| 22 | TCP | SSH (y SFTP) |
| 23 | TCP | Telnet (sin cifrar, en desuso) |
| 25 | TCP | SMTP (envío de correo entre servidores) |
| 53 | UDP y TCP | DNS |
| 67 / 68 | UDP | DHCP (servidor / cliente) |
| 69 | UDP | TFTP |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 123 | UDP | NTP (hora) |
| 143 | TCP | IMAP |
| 161 | UDP | SNMP |
| 389 | TCP | LDAP |
| 443 | TCP | HTTPS |
| 445 | TCP | SMB (carpetas compartidas de Windows) |
| 465 | TCP | SMTPS (SMTP con TLS) |
| 587 | TCP | SMTP de envío desde el cliente de correo |
| 636 | TCP | LDAPS |
| 993 | TCP | IMAPS |
| 995 | TCP | POP3S |

> ➕ **Ampliación:** rangos de puertos:
>
> - **0-1023**, bien conocidos. En Linux, solo `root` puede abrir un puerto de este rango. Por eso en clase usamos el **4444**.
> - **1024-49151**, registrados. Por ejemplo, PostgreSQL 5432, MySQL 3306, o el 8069 que usa Odoo.
> - **49152-65535**, dinámicos o efímeros. Son los que el sistema operativo da al cliente como puerto de origen. Linux usa por defecto del 32768 al 60999.

---

## 6. Ver los paquetes con un *sniffer*: los flags de TCP

Un ***sniffer*** (`tcpdump`, Wireshark) captura los paquetes que pasan por una interfaz de red y muestra sus cabeceras. Con él se ve todo lo anterior: IP y puerto de origen y destino, el *handshake* y la confirmación de los datos.

| Campo | Significado |
|---|---|
| `Flags [S]` | **SYN**: pide abrir una conexión (paso 1 del *handshake*) |
| `Flags [S.]` | **SYN + ACK**: el servidor acepta (paso 2). El `.` significa **ACK** |
| `Flags [.]` | Solo **ACK**: confirma lo recibido (paso 3 y confirmaciones de datos) |
| `Flags [P.]` | **PSH + ACK**: lleva datos y pide entregarlos ya a la aplicación |
| `Flags [F.]` | **FIN + ACK**: cierre ordenado de la conexión |
| `Flags [R]` / `[R.]` | **RST**: corta la conexión de golpe. Es lo que responde el sistema si **nadie escucha en ese puerto** |
| `seq` | Número de secuencia: posición del primer octeto de ese paquete |
| `ack` | Número de confirmación: siguiente octeto que se espera recibir del otro lado |
| `win` | Ventana: cuántos octetos más puede recibir sin confirmar (control de flujo) |
| `options [...]` | Opciones de TCP: `mss` (tamaño máximo de segmento), `sackOK`, `TS val … ecr …` (marca de tiempo propia y **eco** de la del otro lado, *echo reply*), `nop` (relleno sin efecto, para alinear las opciones) y `wscale` (multiplicador de la ventana) |

### Cuando el otro lado también responde

Si en el puerto **no escucha nadie**, a nuestro `[S]` se responde con un `[R.]` y no hay conexión. Si **hay un servidor escuchando**, se ve el *handshake* completo: `[S]` → `[S.]` → `[.]`.

Prueba propuesta para verlo (en tres terminales):

```bash
sudo tcpdump -i lo -n tcp port 4444     # terminal 1: capturar en la interfaz local
python3 servidor.py                      # terminal 2: el servidor del apartado 7
nc 127.0.0.1 4444                        # terminal 3: el cliente
```

> ⏳ **Pendiente:** pegar aquí la salida real de `tcpdump`, primero sin el servidor (debe salir `[R.]`) y después con él (`[S]`, `[S.]`, `[.]`).

---

## 7. Primer servidor en Python (`servidor.py`)

### Ejemplo 1: socket de escucha TCP en el puerto 4444 (`servidor.py`)

```python
import socket

# AF_INET     -> IPv4
# SOCK_STREAM -> TCP   (SOCK_DGRAM -> UDP)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Dónde escuchar: "" (o "0.0.0.0") = en todas las IP que tenga la máquina, puerto 4444
servidor.bind(("", 4444))

# A partir de aquí el socket ya está escuchando
servidor.listen()

# Sin esto el programa terminaría y se cerraría el socket
a = input("aquí esperando")
```

| Línea | Qué hace |
|---|---|
| `socket.socket(AF_INET, SOCK_STREAM)` | Crea el socket: familia **IPv4** (`AF_INET6` sería IPv6) y tipo **TCP** |
| `bind(("", 4444))` | Lo asocia a una IP y un puerto. `""` o `"0.0.0.0"` = **cualquier IP de la máquina**. `"127.0.0.1"` solo aceptaría conexiones desde el propio equipo |
| `listen()` | Lo convierte en **socket de escucha**: el sistema empieza a aceptar conexiones en el puerto 4444 |
| `input(...)` | Deja el programa (y el socket) vivo para poder comprobarlo desde otra terminal |

Todavía **no hay `accept()`**, así que el programa no habla con ningún cliente. Solo se comprueba que el puerto está abierto. Salida real de `ss -putnl` con el servidor en marcha (clase del 05/11, versión anterior con `bind(("0.0.0.0", 4444))`; se dejan solo las líneas relevantes):

```
Netid   State    Recv-Q   Send-Q     Local Address:Port      Peer Address:Port  Process
tcp     LISTEN   0        128              0.0.0.0:4444           0.0.0.0:*      users:(("python3",pid=25805,fd=3))
tcp     LISTEN   0        128              0.0.0.0:22             0.0.0.0:*
tcp     LISTEN   0        200            127.0.0.1:5432           0.0.0.0:*
```

- `ss -putnl`: `-p` proceso, `-u` UDP, `-t` TCP, `-n` números (sin traducir a nombres), `-l` solo los que escuchan.
- `LISTEN 0.0.0.0:4444` de `python3`: es nuestro socket de escucha, en todas las IP. El `Peer Address` `0.0.0.0:*` indica que aún no hay nadie al otro lado.
- `127.0.0.1:5432` (PostgreSQL) solo escucha en local, y `0.0.0.0:22` (SSH) en todas las IP.
- En un socket `LISTEN`, `Send-Q` es el tamaño máximo de la cola de conexiones pendientes (128) y `Recv-Q`, cuántas hay esperando ahora mismo.

> ➕ **Ampliación:**
>
> - El *handshake* lo completa el **sistema operativo**, no el programa. Con solo `listen()`, un `nc 127.0.0.1 4444` **sí conecta**: la conexión se queda en la cola (`Recv-Q` pasa a 1) hasta que el programa la recoja con `accept()`, que devuelve el **socket de conexión** y la dirección del cliente. Ese será el siguiente paso.
> - Con `SOCK_DGRAM` (UDP) **no se usa `listen()`**: no hay conexiones, se reciben datagramas sueltos con `recvfrom()`.

---

## 8. Aceptar una conexión: `accept()`

### Qué pasa cuando llega un cliente

Repaso de la clase del 10/11: cada paquete lleva **IP origen, IP destino, puerto origen, puerto destino y los datos** (*payload*).

> ✏️ **Corrección:** en las notas aparece «el cliente, cuando envía un datagrama, su IP src no está definida; usa el que esté libre». Lo que no fija el cliente es el **puerto** de origen: el sistema operativo le asigna uno **efímero** libre (en clase salió el **48203**). La IP de origen es la de la interfaz por la que sale el paquete. En cambio, el servidor **sí tiene que fijar** su puerto con `bind()`, porque el cliente tiene que saber a dónde llamar.

Cuando el paquete llega al servidor, el sistema operativo ve que hay alguien escuchando en ese puerto, pero **no le pasa los datos directamente al programa**: completa el *handshake*, guarda la conexión en la **cola** del socket de escucha y los datos que van llegando en un **búfer del núcleo**. El programa los va **pidiendo** cuando quiere (`accept()`, `recv()`).

### Ejemplo 2: aceptar un cliente (`servidorAccept.py`)

```python
import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("", 4444))
servidor.listen()

# Se bloquea aquí hasta que llegue un cliente
socket_cliente, addr = servidor.accept()

print(f"IP_Cliente= {addr[0]} Puerto_Cliente= {addr[1]} Protocolo= TCP")
a = input("aquí esperando")
```

| Línea | Qué hace |
|---|---|
| `servidor.accept()` | Saca de la cola la primera conexión ya establecida. Si la cola está vacía, **el programa se queda bloqueado** en esta línea (por eso el `input()` no se ejecuta hasta que alguien conecta) |
| `socket_cliente` | Un socket **nuevo y distinto**: el **socket de conexión** con ese cliente (apartado 4). Por él se reciben y envían los datos |
| `addr` | Tupla `(ip, puerto)` **del cliente**: `addr[0]` es su IP y `addr[1]` su puerto efímero |

Hay por tanto **dos sockets**:

| Socket | Para qué sirve |
|---|---|
| `servidor` (escucha) | Solo **recoge peticiones de conexión** y las deja en la cola. Nunca lleva datos |
| `socket_cliente` (conexión) | Lleva los **datos** de un cliente concreto. El SO le asocia las 4 direcciones y el búfer donde están los datos recibidos |

> ✏️ **Corrección (código del repo):** en `servidorAccept.py` y `servidorAcceptRespuesta.py` la variable se llama `addre` en el `accept()` pero luego se usa `addr[0]`: al conectar un cliente salta `NameError: name 'addr' is not defined`. Hay que usar el mismo nombre en las dos líneas (aquí, `addr`). En `servidorAccept.py` sobra además una `}` al final del `print` (saldría `TCP}`).

**Prueba en clase:** el profesor lanzó el servidor y un alumno conectó desde su PC con `nc <ip_del_profesor> 4444`. En la terminal del profesor salió la IP del alumno y el puerto **48203** (el efímero que eligió su sistema). Un segundo alumno conectó también: su `nc` **conectó** (el SO hace el *handshake* y lo deja en la cola), pero el programa ya no lo atendía porque solo hay **un** `accept()`.

---

## 9. Recibir y responder: `recv()`, `sendall()` y la codificación

### Ejemplo 3: leer el mensaje y contestar (`servidorAcceptRespuesta.py`)

```python
import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("", 4444))
servidor.listen()

socket_cliente, addr = servidor.accept()
print(f"IP_Cliente= {addr[0]} Puerto_Cliente= {addr[1]} Protocolo= TCP")

datos = socket_cliente.recv(1024)          # bloqueante: espera a que el cliente envíe algo
print(datos.decode("utf-8"))               # bytes -> texto
socket_cliente.sendall("Mensaje recibido".encode("utf-8"))  # texto -> bytes
socket_cliente.close()                     # cierra la conexión con ESTE cliente

a = input("aquí esperando")

socket_cliente, addr = servidor.accept()   # segundo cliente
print(f"IP_Cliente= {addr[0]} Puerto_Cliente= {addr[1]} Protocolo= TCP")
```

| Llamada | Qué hace |
|---|---|
| `recv(1024)` | Pide al SO **hasta** 1024 octetos del búfer de esa conexión. **Bloquea** si aún no ha llegado nada. Devuelve `bytes`; si devuelve `b""`, el cliente ha cerrado |
| `decode("utf-8")` | Convierte los `bytes` recibidos en `str` |
| `encode("utf-8")` | Convierte un `str` en `bytes`: por la red solo viajan octetos |
| `sendall(...)` | Envía **todos** los octetos (a diferencia de `send()`, que puede enviar solo una parte y devuelve cuántos) |
| `close()` | Cierra el socket de conexión: el `nc` del alumno termina y le devuelve la terminal. El socket de escucha sigue abierto |

En clase: el alumno escribe en su `nc`, el texto aparece en la terminal del profesor y al alumno le llega «Mensaje recibido». Después se repite con el segundo alumno.

> ➕ **Ampliación:** TCP es un **flujo de octetos**, no de mensajes. Un `recv(1024)` puede traer medio mensaje o dos juntos; en un protocolo real se marca dónde acaba cada mensaje (un salto de línea, la longitud al principio…).

### ASCII y UTF-8

| Caracteres | Octetos en UTF-8 | Ejemplo |
|---|---|---|
| ASCII (letras inglesas, números, signos básicos) | 1 | `a` |
| Latinos con tilde, `ñ`, griego, cirílico… | 2 | `ñ` |
| Resto del plano básico (`€`, chino, japonés…) | 3 | `€` |
| Emojis y otros | 4 | `😀` |

UTF-8 es compatible con ASCII (un texto solo con caracteres ASCII ocupa lo mismo en los dos). Lo importante es que **los dos lados usen la misma codificación**: si se codifica en UTF-8 y se decodifica con otra, las tildes y la `ñ` salen mal.

> ✏️ **Corrección:** en el comentario del código pone `.decode('utf-9')`: no existe, es `utf-8`.

### «Address already in use» al relanzar el servidor

Si se para el servidor y se vuelve a lanzar enseguida, `bind()` puede fallar con `OSError: [Errno 98] Address already in use`. Las conexiones cerradas quedan un rato en estado **`TIME_WAIT`** (hasta un par de minutos) y por defecto el núcleo no deja reutilizar ese puerto. Es lo que se buscó en clase cómo desactivar; se hace **antes del `bind()`** con:

```python
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

> 🧪 **Prueba local (Windows, Python, 10/11/2026)** con la versión corregida, un bucle de 2 `accept()` y un cliente Python en `127.0.0.1`: los dos clientes recibieron «Mensaje recibido» y el servidor mostró los puertos efímeros 54169 y 54170 (consecutivos: el SO los va asignando). ⏳ Pendiente repetirlo en Linux con `nc` y pegar aquí la salida real.

---

## 10. El problema: un cliente cada vez

Con este servidor, **si el primer cliente no termina, el segundo espera** todo lo que haga falta: el programa está bloqueado en el `recv()` del primero y no vuelve al `accept()`.

Primera mejora, un bucle para no repetir el `accept()`:

```python
while True:
    socket_cliente, addr = servidor.accept()   # el hilo principal se bloquea aquí
    atender(socket_cliente, addr)              # mientras atiende a uno, nadie más entra
```

La solución es usar lo de la **UT1**: el hilo principal solo hace `accept()` y **entrega cada socket de conexión a un hilo nuevo**, que lo atiende mientras el principal vuelve a esperar al siguiente. Con un `threading.Semaphore(n)` se limita cuántos clientes se atienden a la vez.

```python
import threading

while True:
    socket_cliente, addr = servidor.accept()
    threading.Thread(target=atender, args=(socket_cliente, addr)).start()
```

> Según el profesor, el servidor concurrente se verá en detalle en la **UT4**. Por eso se explica primero TCP: está pensado para conexiones que se atienden por separado (un socket por cliente); UDP no tiene conexiones.

---

## Resumen rápido

- **Cliente-servidor:** el servidor escucha en un puerto conocido y el cliente **inicia** la comunicación.
- Para llegar a un proceso hacen falta **IP** (máquina) + **TCP o UDP** + **puerto** (proceso). Los puertos TCP y UDP son independientes.
- **TCP:** con conexión (*three-way handshake* `SYN` → `SYN-ACK` → `ACK`), numera los octetos (`seq`/`ack`) y reenvía lo perdido. **UDP:** sin conexión ni confirmación.
- La **IP** va en la cabecera IP y los **puertos** en la de TCP/UDP. El servidor conoce la IP y el puerto del cliente por el primer paquete y responde **intercambiando origen y destino**.
- **Socket de escucha** = `[ip, puerto]`. **Socket de conexión** = `[ip_origen, puerto_origen, ip_destino, puerto_destino]`. Muchas conexiones pueden compartir el puerto del servidor.
- **Puertos bien conocidos** 0-1023 (solo `root` en Linux): 22 SSH, 53 DNS, 80 HTTP, 443 HTTPS… Sin puerto en la URL, el navegador usa el del protocolo.
- **`tcpdump`:** `[S]` SYN, `[S.]` SYN-ACK, `[.]` ACK, `[P.]` datos, `[F.]` cierre, `[R]` rechazo (nadie escucha). `win` = ventana, `TS val/ecr` = marcas de tiempo, `nop` = relleno.
- `socket.socket(AF_INET, SOCK_STREAM)` → `bind(("", 4444))` (`""` = todas las IP) → `listen()` → `accept()`. Se comprueba con `ss -putnl`.
- `accept()` **bloquea** hasta que llega un cliente y devuelve `(socket_cliente, addr)`: un **socket de conexión nuevo** y la IP y el puerto efímero del cliente. El de escucha solo recoge conexiones.
- `recv(1024)` (bloqueante, devuelve `bytes`) + `decode("utf-8")`; `sendall(texto.encode("utf-8"))`; `close()` libera al cliente. UTF-8: 1 octeto en ASCII, 2-4 en el resto.
- `SO_REUSEADDR` antes de `bind()` evita «Address already in use» al relanzar.
- Con un solo hilo se atiende **un cliente cada vez**; la solución es un hilo por cliente tras cada `accept()` (UT4).
