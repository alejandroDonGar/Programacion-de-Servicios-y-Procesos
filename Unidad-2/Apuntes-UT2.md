# UT2 · Comunicación en red: sockets

Apuntes de Programación de Servicios y Procesos (2º DAM 2026-2027), a partir de las notas de clase del 26/10, el 05/11 y el 09/11/2026.

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

## Resumen rápido

- **Cliente-servidor:** el servidor escucha en un puerto conocido y el cliente **inicia** la comunicación.
- Para llegar a un proceso hacen falta **IP** (máquina) + **TCP o UDP** + **puerto** (proceso). Los puertos TCP y UDP son independientes.
- **TCP:** con conexión (*three-way handshake* `SYN` → `SYN-ACK` → `ACK`), numera los octetos (`seq`/`ack`) y reenvía lo perdido. **UDP:** sin conexión ni confirmación.
- La **IP** va en la cabecera IP y los **puertos** en la de TCP/UDP. El servidor conoce la IP y el puerto del cliente por el primer paquete y responde **intercambiando origen y destino**.
- **Socket de escucha** = `[ip, puerto]`. **Socket de conexión** = `[ip_origen, puerto_origen, ip_destino, puerto_destino]`. Muchas conexiones pueden compartir el puerto del servidor.
- **Puertos bien conocidos** 0-1023 (solo `root` en Linux): 22 SSH, 53 DNS, 80 HTTP, 443 HTTPS… Sin puerto en la URL, el navegador usa el del protocolo.
- **`tcpdump`:** `[S]` SYN, `[S.]` SYN-ACK, `[.]` ACK, `[P.]` datos, `[F.]` cierre, `[R]` rechazo (nadie escucha). `win` = ventana, `TS val/ecr` = marcas de tiempo, `nop` = relleno.
- `socket.socket(AF_INET, SOCK_STREAM)` → `bind(("", 4444))` (`""` = todas las IP) → `listen()` → (pendiente) `accept()`. Se comprueba con `ss -putnl`.
