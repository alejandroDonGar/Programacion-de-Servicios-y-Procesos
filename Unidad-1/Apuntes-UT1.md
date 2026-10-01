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
> ➕ **Ampliación:** la forma correcta de que el padre **espere a que termine el hijo** es `os.wait()`:
>
> ```python
> else:
>     os.wait()  # El padre se bloquea hasta que el hijo termine
>     print("Soy el padre y mi hijo ya ha terminado")
> ```
>
> Si el padre no espera al hijo, el hijo queda como **zombie** (`Z` en `ps`) hasta que alguien recoge su estado de salida.

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

---

iteraciones <- programa 2

---
programa 3 \/
Pid, status = os.wait() -> estoy esperando a que los hijos del fork terminen

pid se queda con el identificador dl procesos
status se queda con el estado de la salida.

sys

codigo = os.waitstatus_to_exitcode(status) -> cambia el estado codificado del numero a exitcode

---