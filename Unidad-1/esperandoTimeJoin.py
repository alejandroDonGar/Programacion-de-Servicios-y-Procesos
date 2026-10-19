import threading,time

def hilo_secundario():
	for i in range(1000):
		print("Y", end="",flush=True) # Escribirá 1000 veces la letra 'Y'
				# Usando flush, en vez de meter las 1000 ordenes de entrada y salida
				# en una sola linea, manda 1 a 1 las ordenes.
				# Ahora al ser 1 a 1, el sistema puede sacarlo y traer al ultimo print 'El hilo secundario ya terminó, ¡ADIÓS!' aunque no hya terminado.
t = threading.Thread(target=hilo_secundario,daemon=False)
						# Con flase espera por el join()
						# Con 'True' va a esperar igualmente
						# El join() siempre va a obligar al main a esperar independientemente del daemon 
t.start()

for i in range(10): # Hilo printipal
	print("X", end="",flush=True)

#¿Ahora como hacemos para que este 'print("El hilo secundario ya terminó, ¡ADIÓS!")' salga siempre el último?
# Así \/
t.join() # Este join automaticamente hace esperar al principal a que espere al secundario
print("El hilo secundario ya terminó, ¡ADIÓS!") # Queremos que esta sea la última ejecucion del proceso
