import threading,time

hilos=[]

def otro_hilo():
	for i in range(1000):
		time.sleep(0.001)
		print(f"Y={i}", end="", flush=True) # Por si solo no hace nada porque no lo hemos llamado todavia

t = threading.Thread(target=otro_hilo,daemon=True) # Crea el hilo.
t.start() # Ahora esta ejecutado

hilos.append(t) # Añadimos el hilo 1 a la lista
print(t.name) # Imprime el nombre del hilo
# Main thread
for i in range(1000):
	time.sleep(0.001)
	print(f"X={i}", end="", flush=True)

print("\n", end="")

t = threading.Thread(target=otro_hilo)
t.start()
hilos.append(t) # Añadimos el hilo 2 a la lista
print(t.name)

for hilo in hilos:
	print(hilo.name) # Por acad hilo dentro de la lista nos dara el nombre

# Tras el t.start() no hay orden en el que puedan salir los dos, tal vez sale el for primero y luego el def, o al revés
