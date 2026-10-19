import threading

def hilo_secundario():
	for i in range(1000):
		print("Y", end="") # Escribirá 1000 veces la letra 'Y'

t = threading.Thread(target=hilo_secundario,daemon=False)
t.start()

print("X", end="")
print("El hilo secundario ya terminó, ¡ADIÓS!") # Queremos que esta sea la última ejecucion del proceso
