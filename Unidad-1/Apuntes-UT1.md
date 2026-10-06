# UT1 · Procesos y concurrencia

Apuntes de Programación de Servicios y Procesos (2º DAM 2026-2027), a partir de las notas de clase del 17/09/2026.

> 📚 Libro de referencia: *Programación de Servicios y Procesos en Python*.

> ✏️ Los bloques marcados como **Corrección** arreglan algo que quedó mal apuntado en clase. Los de **Ampliación** añaden algo que no se dio pero ayuda a entenderlo.

---

## 1. Arquitectura Von Neumann

Es el modelo en el que se basan casi todos los ordenadores: **la CPU, una memoria principal donde están a la vez los datos y las instrucciones, y los dispositivos de entrada/salida**, conectados por buses.

```
         ┌───────┐        ┌───────────────────┐
         │  CPU  │────────│ Memoria principal │   (datos + instrucciones juntos)
         └───┬───┘        └───────────────────┘
             │
         ┌───┴───┐
         │  E/S  │──┬──> red
         └───────┘  ├──> teclado
                    └──> disco duro (HDD)
```

Como datos e instrucciones van por **el mismo bus**, la CPU no puede leer una instrucción y un dato a la vez. A esto se le llama el *cuello de botella de Von Neumann*.

### Registros importantes de la CPU

| Registro | Nombre | Qué guarda |
|---|---|---|
| **PC** | *Program Counter* (contador de programa) | La **dirección de memoria de la siguiente instrucción** que se va a ejecutar. Cada vez que se ejecuta una, avanza. |
| **RI** | Registro de Instrucción | La **instrucción que se está ejecutando ahora mismo**. La CPU la trae de la dirección a la que apunta el PC, la copia aquí, la decodifica y la ejecuta. |
| **SP** | *Stack Pointer* (puntero de pila) | La dirección de la **cima de la pila**. |

> ✏️ **Corrección:** la pila es **LIFO**, *Last In, First Out* (el último que entra es el primero que sale), como una pila de platos. En las notas ponía "first in last out", que es la misma idea dicha al revés. El nombre oficial es LIFO.
>
> En la mayoría de CPUs la pila **crece hacia direcciones más bajas**. Por eso en el ejemplo de clase el SP baja: 1500 → 1499 → 1498…

### Evolución para ganar velocidad

1. **Una instrucción detrás de otra:** lento, porque ir a la memoria principal cuesta mucho tiempo.
2. **Memoria caché:** se copian bloques de memoria a una memoria pequeña y muy rápida **dentro de la propia CPU**.
3. **Varios núcleos:** en lugar de un solo "centro de proceso", se meten varios en la misma CPU. Cada uno puede ejecutar su propio programa.

---

## 2. Cómo "trabajan a la vez" dos programas con una sola CPU

Ejemplo de clase: dos programas cargados en memoria a la vez.

```
Programa 1 (dirección 1000)     Programa 2 (dirección 2000)
mov a, var1                     mov a, 27
mov b, var2                     mov b, a
sum a, b                        sum a, b
mov var3, a                     mov var4, a

var1 = 100
var2 = 200
```

**El problema:** si ejecutamos parte del programa 1, saltamos al programa 2 (PC = 2000) y luego volvemos, los registros `a` y `b` ya tienen los valores que dejó el programa 2. El programa 1 continuaría con datos que no son suyos y daría un resultado incorrecto.

**La solución: el cambio de contexto.**

1. Antes de pausar el programa 1, se **guarda su contexto** (los registros `a`, `b` y el PC con la instrucción por la que iba) en su zona de la pila. En el ejemplo: pila en 1500, se guarda `100`, `200` y la dirección de vuelta `1002`.
2. Se apunta que ese contexto pertenece al **programa 1**.
3. Se carga el programa 2 y se ejecuta un rato. Cuando toca pausarlo, se guarda **su** contexto de la misma forma (pila en 2500: `27`, `27`, `2002`).
4. Para volver al programa 1, se **restauran** sus registros y su PC desde la pila, y sigue exactamente donde lo dejó.

El sistema operativo hace esto miles de veces por segundo. Como cambia tan rápido, **parece que los dos programas se ejecutan a la vez**. Eso es la **ejecución concurrente**.

> ✏️ **Corrección:** en las notas pone "Pila → 1487" entre 1498 y la siguiente posición. Es una errata: debería ser **1497**, porque cada valor guardado baja una posición.

### El PCB: dónde guarda el sistema operativo cada proceso

Quien controla todo esto es el **sistema operativo**. Para cada proceso mantiene un **PCB** (*Process Control Block*, bloque de control del proceso), donde está **toda la información del proceso**: su PID, su estado, sus registros guardados, el PC, dónde está en memoria…

- El **sistema operativo asigna las posiciones de memoria** que ocupa cada proceso.
- Cuando hay un cambio de contexto, la CPU **guarda los registros en la pila del proceso** (antes de que el kernel entre a trabajar) y los restaura al volver. La pila se gestiona con el registro **SP** y es **LIFO**.
- Dentro de la memoria de un proceso hay varias zonas:

```
PC ──> código        (las instrucciones del programa; el PC apunta a la que toca)
       datos
       variables
       pila   <── SP (LIFO: crece hacia direcciones más bajas)
```

Esto es clave para entender dos cosas que vienen después: **`fork` copia el PCB** (sección 5) y un **hilo** reparte el PC dentro de un mismo PCB (sección 6).

### Concurrencia y paralelismo

| | **Concurrencia** | **Paralelismo** |
|---|---|---|
| Qué es | Varios procesos **avanzan intercalándose** en el tiempo | Varios procesos se ejecutan **en el mismo instante** |
| Núcleos mínimos | **1** | **2 o más** |
| Cómo se consigue | Cambios de contexto rápidos | Cada proceso en su propio núcleo o hilo hardware |

---

## 3. Ver los procesos en Linux

### `top`: procesos en directo

Muestra los procesos **actualizándose en tiempo real**, ordenados por uso de CPU. Se sale con `q`.

### `ps aux`: foto fija de todos los procesos

Muestra **todos los procesos en el instante en que lo ejecutas**.

| Columna | Significado |
|---|---|
| `USER` | Usuario dueño del proceso |
| `PID` | *Process ID*, identificador único del proceso |
| `%CPU` / `%MEM` | Porcentaje de CPU y de memoria que usa |
| `VSZ` | Memoria **virtual** reservada (KiB) |
| `RSS` | Memoria **física** (RAM) que ocupa de verdad (KiB) |
| `STAT` | Estado: `R` ejecutándose, `S` dormido/esperando, `D` esperando E/S, `T` parado, `Z` zombie |
| `START` | Hora a la que arrancó |
| `TIME` | Tiempo total de CPU que ha consumido |
| `COMMAND` | El comando que lo lanzó |

**Filtrar con `grep`:**

```bash
ps aux | grep alejandro    # líneas que contengan "alejandro"
ps aux | grep python       # procesos de python
```

> ✏️ **Corrección:** `grep` no filtra "por columna", sino **cualquier línea que contenga ese texto**, esté en la columna que esté. Para filtrar de verdad por usuario o por PID:
>
> ```bash
> ps -u alejandro     # procesos de un usuario
> ps -p 1234          # un PID concreto
> ```

### `ps -efl`: más columnas

- `-e`: todos los procesos.
- `-f`: formato completo, que incluye el **PPID** (*Parent PID*, el PID del proceso padre).
- `-l`: formato largo, que incluye el estado (`S`), **PRI** y **NI**.

**Prioridad:**

- **PRI:** prioridad del proceso. Por defecto vale **80**. **Cuanto más bajo, más prioridad**.
- **NI** (*nice*): valor que **se suma a la prioridad** para subirla o bajarla. Va de **-20** (más prioridad) a **19** (menos prioridad). Por defecto es 0.

> ➕ **Ampliación:** para cambiar el *nice*:
>
> ```bash
> nice -n 10 python3 programa.py   # lanzar con menos prioridad
> renice -n 5 -p 1234              # cambiar la de un proceso que ya existe
> ```
>
> Para poner valores negativos (más prioridad) hace falta `sudo`.

---

## 4. La CPU por dentro: `lscpu`

`lscpu` muestra la información del procesador. Datos importantes del ordenador de clase (**AMD Ryzen 5 PRO 4650G**):

| Dato | Valor | Qué significa |
|---|---|---|
| Arquitectura | `x86_64` | Procesador de 64 bits (puede ejecutar también código de 32) |
| Núcleos por socket | **6** | 6 núcleos físicos |
| Hilos por núcleo | **2** | Cada núcleo ejecuta 2 hilos a la vez (SMT) |
| CPU(s) | **12** | 6 núcleos × 2 hilos = 12 CPUs lógicas |
| Virtualización | AMD-V | Soporte por hardware para máquinas virtuales |

### ¿Cuántos procesos a la vez?

- **En paralelo de verdad:** hasta **12** (uno por CPU lógica). Los 2 hilos de un mismo núcleo comparten sus recursos, así que no rinden como 2 núcleos completos. Si los hilos no compiten por lo mismo, se acercan bastante.
- **Concurrentes:** **muchísimos más**. El sistema operativo los va turnando con cambios de contexto. Ahora mismo tu ordenador tiene cientos de procesos (míralo con `ps aux | wc -l`).

> ✏️ **Corrección:** en las notas pone "6 procesos en paralelo o 12 concurrentes". Con SMT son **12 hilos en paralelo** (6 núcleos completos). El número de procesos concurrentes **no tiene ese límite**.

### Bits y número de combinaciones

Con **n bits** se pueden representar **2ⁿ** valores distintos:

| Bits | Combinaciones |
|---|---|
| 1 | 2¹ = 2 |
| 2 | 2² = 4 |
| 3 | 2³ = 8 |
| 8 | 2⁸ = **256** |
| 16 | 2¹⁶ = 65 536 |
| 32 | 2³² = **4 294 967 296** (≈ 4 mil millones) |
| 64 | 2⁶⁴ ≈ 1,8 × 10¹⁹ |

- Con instrucciones de **8 bits** hay **256** instrucciones posibles.
- Con direcciones de **32 bits** se pueden direccionar unos **4 mil millones** de posiciones, es decir, **4 GiB** de memoria. Por eso los sistemas de 32 bits no podían usar más de 4 GB de RAM.

> ✏️ **Corrección:** la tabla de potencias de las notas estaba desalineada (10³ con 2², 10⁴ repetido…). Base 10 y base 2 no se corresponden fila a fila. Lo importante es la regla **n bits → 2ⁿ valores**.

### Memoria caché

```
lscpu → Cachés:
  L1d: 192 KiB (6 instancias)
  L1i: 192 KiB (6 instancias)
  L2:  3 MiB   (6 instancias)
  L3:  8 MiB   (2 instancias)
```

| Nivel | Velocidad | Tamaño | ¿De quién es? |
|---|---|---|---|
| **L1** | La más rápida | La más pequeña | **Una por núcleo** (6 instancias). Dividida en **L1d** (datos) y **L1i** (instrucciones) |
| **L2** | Intermedia | Intermedia | **Una por núcleo** (6 instancias) |
| **L3** | La más lenta de las tres, pero mucho más rápida que la RAM | La más grande | **Compartida** entre varios núcleos |

**Arquitectura Harvard en la L1:** la L1 está separada en instrucciones (L1i) y datos (L1d), con **buses distintos**. Así la CPU puede traer una instrucción y un dato **a la vez, en paralelo**. Fuera de la CPU el ordenador sigue siendo Von Neumann (una sola RAM para todo). Por eso se dice que las CPUs actuales son **Harvard por dentro (L1) y Von Neumann por fuera**.

> ✏️ **Correcciones:**
>
> - La **d** de L1d es de **datos** (*data*), no de "direcciones".
> - La L1 está **dentro de cada núcleo de la CPU**, no en la tarjeta gráfica integrada.
> - La L3 tiene 2 instancias porque este Ryzen agrupa los 6 núcleos en **2 bloques de 3** (CCX). Cada bloque tiene 4 MiB de L3 **compartidos por sus 3 núcleos**. No es "una por núcleo".

---

## 5. Crear procesos en Python: `os.fork()`

`os.fork()` pide al sistema operativo que **clone el proceso actual**. A partir de esa línea hay **dos procesos** ejecutando el mismo código: el **padre** (el original) y el **hijo** (la copia).

### Qué devuelve `fork()`

| Proceso | Valor de `pid` |
|---|---|
| **Hijo** | **0** |
| **Padre** | **El PID del hijo** (un número > 0) |
| Si falla | Lanza una excepción `OSError` |

Así es como cada proceso sabe cuál de los dos es.

> ➕ **Por dentro:** `fork()` **copia el PCB** del padre para crear el del hijo, y le **asigna posiciones de memoria nuevas**. Por eso, aunque el código sea el mismo, cada proceso tiene su propia copia de variables y de pila (ver Ejemplo 4) y un PID distinto.

> ⚠️ `os.fork()` **solo existe en Linux/macOS**. En Windows da error, así que **ejecuta estos programas en WSL** con `python3 programa.py`.

### Ejemplo 1: padre e hijo

```python
import os

pid = os.fork()  # A partir de aquí hay DOS procesos

if pid == 0:
    print("Soy el hijo")
else:
    print("Soy el padre")

print("Los dos")  # Esta línea la ejecutan ambos
```

Dos ejecuciones posibles:

```
Soy el hijo        Soy el padre
Los dos            Soy el hijo
Soy el padre       Los dos
Los dos            Los dos
```

**El orden no está garantizado.** Son dos procesos distintos y el sistema operativo decide cuál ejecuta primero. "Los dos" sale dos veces porque **cada proceso imprime la suya**, no porque uno ejecute el código dos veces.

### Ejemplo 2: ver los PID

```python
import os

pid = os.fork()

if pid == 0:
    # os.getppid() -> PID del padre
    print(f"Soy el hijo, mi PID es {os.getpid()} y el de mi padre es {os.getppid()}")
else:
    # En el padre, 'pid' es el PID del hijo
    print(f"Soy el padre, mi PID es {os.getpid()} y el de mi hijo es {pid}")

print(f"Los dos {os.getpid()}")
```

Salida (los números cambian en cada ejecución):

```
Soy el hijo, mi PID es 5124 y el de mi padre es 5123
Los dos 5124
Soy el padre, mi PID es 5123 y el de mi hijo es 5124
Los dos 5123
```

Fíjate en que el **PID del hijo que ve el padre** (`pid`) coincide con el `os.getpid()` del hijo, y el `os.getppid()` del hijo coincide con el `os.getpid()` del padre.

| Función | Devuelve |
|---|---|
| `os.getpid()` | El PID del proceso actual |
| `os.getppid()` | El PID de su padre |

> ✏️ **Corrección:** en las notas aparece `os.getPid()` con P mayúscula y `os.getppid` sin paréntesis. En Python es **`os.getpid()`** en minúsculas, y **las funciones hay que llamarlas con `()`**. Sin paréntesis imprimiría algo como `<built-in function getppid>` en vez del número.

### Ejemplo 3: forzar el orden con `time.sleep()`

`time.sleep(n)` **detiene el proceso n segundos**:

```python
import time

print("Inicio del programa")
time.sleep(3)  # Pausa de 3 segundos
print("Han pasado 3 segundos")
```

Si el **padre duerme 2 segundos**, el hijo casi siempre termina antes:

```python
import os
import time  # ¡Hay que importarlo!

pid = os.fork()

if pid == 0:
    print(f"Soy el hijo, mi PID es {os.getpid()} y el de mi padre es {os.getppid()}")
else:
    time.sleep(2)  # El padre se bloquea 2 segundos
    print(f"Soy el padre, mi PID es {os.getpid()} y el de mi hijo es {pid}")

print(f"Los dos {os.getpid()}")
```

```
Soy el hijo, mi PID es 5124 y el de mi padre es 5123
Los dos 5124
Soy el padre, mi PID es 5123 y el de mi hijo es 5124
Los dos 5123
```

**Por qué funciona:** al hacer `sleep`, el padre pasa a estado **bloqueado** (`S` en `ps`) y el sistema operativo lo **saca de la CPU**. La CPU queda libre para el hijo, que en 2 segundos tiene tiempo de sobra para terminar.

> ✏️ **Matiz:** `sleep` hace que ese orden sea **muy probable**, pero no lo **garantiza**. Si el sistema estuviera muy cargado, el hijo podría tardar más de 2 segundos.
>
> La forma correcta de que el padre **espere a que termine el hijo** es `os.wait()`, que se vio en la clase siguiente (**Ejemplo 5**).

### Ejemplo 4: procesos intercalados (`programa2.py`)

Padre e hijo hacen **10 iteraciones cada uno** a la vez, pero a distinto ritmo: el hijo duerme 1 segundo entre vuelta y vuelta y el padre, 2.

```python
import os, time

pid = os.fork()

if pid == 0:
    # Hijo: una iteración por segundo
    for i in range(10):              # i va de 0 a 9 → 10 vueltas
        print(f"Hijo {os.getpid()}. Iteración {i}")
        time.sleep(1)
else:
    # Padre: una iteración cada 2 segundos
    for i in range(10):
        print(f"Padre {os.getpid()}. Iteración {i}")
        time.sleep(2)
```

Salida aproximada (los PID cambian):

```
Padre 5123. Iteración 0
Hijo 5124. Iteración 0
Hijo 5124. Iteración 1
Padre 5123. Iteración 1
Hijo 5124. Iteración 2
Hijo 5124. Iteración 3
Padre 5123. Iteración 2
...
Hijo 5124. Iteración 9         ← el hijo termina hacia el segundo 10
Padre 5123. Iteración 5
...                            ← el padre sigue solo hasta el segundo 20
Padre 5123. Iteración 9
```

**Qué demuestra:**
- Los dos procesos avanzan **a la vez** y sus mensajes salen **intercalados**. Es la **concurrencia** de la sección 2, ahora vista con tus propios procesos.
- Cada `sleep` **bloquea** solo al proceso que lo llama y le deja la CPU al otro. Por eso el hijo, que duerme menos, imprime unas **dos líneas por cada una del padre**.
- **Cada proceso tiene su propia copia de las variables:** la `i` del hijo y la del padre son distintas. Tras el `fork` no comparten memoria.
- El hijo termina hacia el segundo 10 y el padre sigue solo hasta el 20. Como el padre **no hace `wait()`**, mientras sigue vivo el hijo ya terminado se queda como **zombie**. Compruébalo en otra terminal con `ps -efl | grep python` mientras se ejecuta: verás el hijo en estado `Z` y marcado como `<defunct>`.

### Ejemplo 5: el padre espera al hijo con `os.wait()` (`programa3.py`)

```python
import os, time, sys

pid = os.fork()

if pid == 0:
    # Hijo
    print(f"PID: {os.getpid()}")
    nombre = input("Ingrese su nombre: ")
    time.sleep(5)
    print(f"El proceso hijo va a terminar. Has escrito {nombre}")
    sys.exit(5)                          # termina el hijo con código de salida 5
else:
    # Padre
    pid, status = os.wait()              # se BLOQUEA hasta que termine un hijo
    codigo = os.waitstatus_to_exitcode(status)
    print(f"Soy el padre con PID: {os.getpid()}. El hijo ha terminado con PID: {pid} y estado: {codigo}")
```

```
PID: 5124
Ingrese su nombre: Alejandro
El proceso hijo va a terminar. Has escrito Alejandro      ← 5 segundos después
Soy el padre con PID: 5123. El hijo ha terminado con PID: 5124 y estado: 5
```

**Paso a paso:**

| Instrucción | Qué hace |
|---|---|
| `os.wait()` | El padre se **bloquea** (estado `S`) hasta que **termina uno de sus hijos**. Por eso el mensaje del padre sale siempre **el último**: aquí el orden **sí está garantizado**, a diferencia del `sleep` del Ejemplo 3 |
| `pid, status = os.wait()` | Devuelve **dos valores** (una tupla) que se reparten en dos variables: `pid` = el PID del hijo que ha terminado · `status` = su estado de salida, **codificado** |
| `sys.exit(5)` | Termina el proceso **hijo** con **código de salida 5**. Es la forma que tiene el hijo de decirle al padre cómo le ha ido |
| `os.waitstatus_to_exitcode(status)` | `status` no es directamente el 5: el sistema lo guarda codificado (para un `exit(5)` vale `5 × 256 = 1280`). Esta función lo **descodifica** y devuelve el código real: `5` |

**Código de salida:** por convenio, **`0` = todo fue bien** y **cualquier otro número = algún error** (cada programa decide qué significa cada uno). En la terminal de Linux puedes ver el código del último programa con `echo $?`.

> ➕ **Por qué es importante el `wait()`:**
> - **Sincroniza:** el padre no sigue hasta que el hijo acaba (por ejemplo, para usar un resultado que calcula el hijo).
> - **Evita zombies:** al recoger el estado del hijo, el sistema puede borrarlo de la tabla de procesos. Sin `wait()`, el hijo terminado queda como **zombie** (`Z`) mientras el padre siga vivo, como pasa en el Ejemplo 4.
> - Si hay **varios hijos**, cada `wait()` recoge **uno** (el primero que termine). Para esperar a un hijo concreto: `os.waitpid(pid_del_hijo, 0)`.

> ✏️ **Detalles:**
> - `os.waitstatus_to_exitcode()` existe desde **Python 3.9**. En versiones anteriores se usaba `os.WEXITSTATUS(status)`.
> - El `input()` lo hace el **hijo**: padre e hijo comparten la misma terminal (la entrada estándar se hereda con el `fork`). Funciona porque el padre está bloqueado en el `wait()` y no lee nada. Si los dos leyeran del teclado a la vez, no se sabría cuál se lleva cada línea.
> - Como `fork()`, `wait()` solo existe en **Linux/macOS**: ejecútalo en **WSL**.

### Ejemplo 6: lanzar un programa externo y medir el tiempo (`programaPing.py`)

`subprocess.run([...])` ejecuta **otro programa** del sistema (aquí `ping`) y **espera a que termine**. El comando se pasa como **lista**: primero el programa y después cada argumento.

```python
import subprocess, time

ahora = time.time()          # tiempo actual, en segundos

# ping -c 1 8.8.8.8  → una sola petición a la IP de Google
for i in range(10):
    subprocess.run(['ping', '-c 1', '8.8.8.8'])   # espera a que acabe antes de la siguiente

# Cuánto ha pasado desde el principio hasta ahora
print(time.time() - ahora)
```

- `-c 1` → *count*: manda **1** paquete y termina (sin esto, `ping` no acabaría nunca en Linux).
- Los 10 pings van **uno detrás de otro**: cada `run` bloquea el programa hasta que su ping termina. El tiempo total es **la suma** de los 10.
- `time.time()` devuelve los segundos desde 1970. Restar el de antes y el de después da **cuánto ha tardado**.

### Ejemplo 7: 10 pings a la vez con `fork` (`programaPing2.py`)

Ahora el padre **crea 10 hijos** y cada uno lanza su ping. Así **se hacen a la vez** en lugar de en fila.

```python
import os, subprocess, time, sys

ahora = time.time()

for i in range(10):
    pid = os.fork()      # el padre crea un hijo y vuelve al bucle a crear el siguiente

    if pid == 0:         # entran SOLO los hijos
        subprocess.run(['ping', '-c 2', '-i 2', '8.8.8.8'])
        sys.exit()       # el hijo termina aquí; si no, seguiría el bucle y crearía sus propios hijos

# Cuando el padre ha creado los 10 hijos, llega aquí
for i in range(10):
    os.wait()            # cada wait() recoge a un hijo que haya terminado

print(time.time() - ahora)
```

**Cómo leerlo:**
- El padre da las 10 vueltas del `for` creando un hijo en cada una. Los hijos pueden arrancar **dentro del mismo *quantum*** (el trocito de tiempo de CPU que da el sistema) o repartidos en varios; no importa, el sistema los va turnando.
- `-c 2 -i 2` → manda **2** paquetes con **2 segundos** de intervalo entre ellos.
- Se forma una cadena **padre → hijo → nieto**: cada hijo lanza `ping` con `subprocess.run`, así que `ping` es el **nieto** del proceso original. En total, 10 hijos y 10 `ping`.
- **`sys.exit()` es imprescindible:** sin él, el hijo terminaría el `subprocess.run` y volvería al `for`, creando más procesos (una "bomba fork").
- Los **10 `os.wait()`** hacen que el padre espere a que acaben los 10 hijos antes de medir el tiempo (así se recogen todos y no quedan zombies).
- **Resultado esperado:** el tiempo total sale parecido al de **un solo** ping (unos 2 segundos de intervalo más el ping), no a la suma de los 10 como en el Ejemplo 6. Es la ventaja de la concurrencia: se aprovechan los tiempos de espera de unos procesos para ejecutar otros. *(Pendiente: pegar aquí los tiempos reales de tu ejecución.)*

> ✏️ **Detalle:** `'-c 2'` (con el espacio dentro de la cadena) es un único argumento. En la práctica `ping` suele aceptarlo, pero lo limpio es separar flag y valor: `['ping', '-c', '2', '-i', '2', '8.8.8.8']`.

---

## 6. Hilos (*threads*)

### El problema de los procesos

Con `fork`, para hacer varias cosas a la vez **clonamos todo el proceso**: nuevo PCB, nueva memoria, nuevo PID. Funciona, pero es pesado, y padre e hijo **no comparten variables** (cada uno tiene su copia).

### La idea del hilo

Dentro del PCB está el código que se va a ejecutar, y el **PC** marca por dónde vamos. Un programa suele tener **varias funciones** que hacen cosas distintas: hacer un ping, imprimir en pantalla, etc. Si las ejecutamos de forma concurrente, hay una alternativa a clonar el proceso:

- En vez de tener **un solo PC**, el proceso tiene **varios PC dentro del mismo PCB**, cada uno apuntando a **una función distinta** (a una posición distinta del código en memoria).
- El sistema puede ir **saltando de uno a otro** manteniendo la coherencia: **mismo proceso, órdenes distintas**.
- Esto se llama **hilo** (*thread*). Si hay 3 PC, hay **3 hilos**: **1 proceso con 3 hilos**.
- Así, en lugar de que un proceso se quede **bloqueado** esperando (y se pierda su turno), otro hilo del mismo proceso puede aprovechar el *quantum*.

```
Proceso (un solo PCB, un solo PID)
├── código, datos, variables  ← compartidos por todos los hilos
├── Hilo 1: su PC y su pila ──> función A (ping)
├── Hilo 2: su PC y su pila ──> función B (imprimir)
└── Hilo 3: su PC y su pila ──> función C
```

| | **Procesos (`fork`)** | **Hilos** |
|---|---|---|
| Memoria | **Copia** distinta para cada uno | **Compartida** (misma memoria del proceso) |
| PID | Uno por proceso | **El mismo** para todos los hilos |
| Relación | Padre e hijo | **No hay padres ni hijos**: es el mismo proceso |
| Coste de crearlos | Alto (se copia el PCB) | Bajo |
| Quién los reparte | El sistema operativo | El sistema operativo (cualquier hilo listo puede ser el siguiente: el orden no está garantizado) |

> ✏️ **Matiz:** en clase se dijo que "el sistema lanza un dado con el número de hilos". Es una forma gráfica de decir que **el orden en que se turnan no está garantizado**. En realidad lo decide el planificador del sistema operativo.
>
> Cada hilo sí tiene **su propio PC y su propia pila** (si no, no sabría por dónde va ni dónde guardar sus variables locales); lo que comparten es el **código y los datos**.

### Ejemplo 8: el primer hilo (`hilo1.py`)

```python
import threading, time

def Saludando():
    # time.sleep(1)  ← si lo ponemos AQUÍ, el hilo principal imprime antes
    print("Hola, soy el hilo secundario")

print("Soy el Main Thread o Hilo Principal")

# Creamos el objeto Thread y le decimos QUÉ función ejecutará (target)
t = threading.Thread(target=Saludando)   # sin paréntesis: pasamos la función, no la llamamos

t.start()   # arranca el hilo: ya está listo para que el sistema le dé CPU

# time.sleep(1)  ← si lo ponemos AQUÍ, el sistema saca al principal y deja trabajar al hilo
print("Soy el Main Thread o Hilo Principal despues")
```

**Paso a paso:**

| Instrucción | Qué hace |
|---|---|
| `threading.Thread(target=Saludando)` | **Crea** el hilo y le asigna la función que ejecutará. Todavía **no corre**. Es como añadir un PC nuevo apuntando a esa función |
| `t.start()` | **Lo lanza**. A partir de aquí hay **dos hilos** en el mismo proceso: el principal (*main thread*) y `t` |
| Hilo principal | Todo programa ya tiene uno: el que ejecuta el código "normal" |

**Qué orden sale:** después de `t.start()`, el hilo secundario **puede o no** ejecutarse antes de que el principal imprima su última línea; **depende de cuándo le dé *quantum* el sistema operativo**. Lo habitual es:

```
Soy el Main Thread o Hilo Principal
Soy el Main Thread o Hilo Principal despues
Hola, soy el hilo secundario
```

pero también puede salir el saludo en medio. Se puede **forzar** con `time.sleep()`:
- `sleep` **dentro de `Saludando`** → el secundario se bloquea y el principal acaba su `print` primero.
- `sleep` **en el principal tras `start()`** → el sistema **saca al principal de la CPU** y el hilo secundario tiene tiempo de imprimir.

Igual que con `fork` y `sleep` (Ejemplo 3), esto hace el orden **muy probable pero no garantizado**. Para esperar de verdad a un hilo se usa `t.join()`, el equivalente de `os.wait()` para hilos.

> ➕ **Diferencia clave con `fork`:** aquí `os.getpid()` valdría **lo mismo** en los dos hilos, porque es **un único proceso**. Con `fork` salían dos PID distintos.

---

## Resumen rápido

- **Von Neumann:** datos e instrucciones en la misma memoria y por el mismo bus.
- **PC** = siguiente instrucción · **RI** = instrucción actual · **SP** = cima de la pila (LIFO).
- **Cambio de contexto:** guardar los registros y el PC de un proceso para retomarlo después. Es lo que hace posible la **concurrencia**.
- **Concurrencia** = turnarse (basta 1 núcleo) · **Paralelismo** = a la vez de verdad (2 o más núcleos).
- `top` (en directo) · `ps aux` (foto fija) · `ps -efl` (con PPID, PRI y NI) · `lscpu` (info de la CPU).
- **PRI** más bajo = más prioridad · **NI** de -20 a 19.
- **n bits → 2ⁿ valores** · 32 bits → 4 GiB.
- Caché **L1** (por núcleo, separada en datos e instrucciones = Harvard) · **L2** (por núcleo) · **L3** (compartida).
- `os.fork()` → **0 en el hijo**, **PID del hijo en el padre** · `os.getpid()` · `os.getppid()` · el orden **no está garantizado**.
- Padre e hijo con bucles y `sleep` → salida **intercalada** (concurrencia); cada uno tiene **sus propias variables**.
- `pid, status = os.wait()` → el padre **espera** a que termine un hijo (orden garantizado, sin zombies) · `sys.exit(n)` → código de salida (0 = bien) · `os.waitstatus_to_exitcode(status)` → descodifica el estado.
- **PCB:** donde el sistema operativo guarda toda la información de un proceso · memoria del proceso = código, datos, variables y pila (SP). `fork` **copia el PCB**.
- `subprocess.run([...])` lanza un programa externo y espera · `time.time()` para medir tiempos · 10 `fork` + 10 `wait()` hacen los pings **a la vez** en lugar de en fila.
- **Hilo:** varios PC dentro del **mismo proceso** (mismo PCB, mismo PID, memoria compartida, sin padre/hijo) · `threading.Thread(target=f)` + `t.start()` (+ `t.join()` para esperar) · el orden entre hilos **no está garantizado**.
