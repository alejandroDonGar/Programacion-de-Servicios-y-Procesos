import threading

dato=0
hilos=[]
lock=threading.Lock()
def suma():
	# Te traes dato, los usas, y terminas. Asi está el proceso controlado y seguro por un unico hilo (sin importar cual), en vez de ir concurrente en esta unica zona.
	# Para eso sirve el 'lock'.
	# El primero que tome la llave ejecuta la suma, y lo unico que se pide es que se deje la llave para el siguiente.

	global dato, lock
	print(f"dato={dato} modificado por {threading.current_thread().name}")
	lock.acquire() # Solicitar el ticker para entrar.
		       # Estas siguientes solo lo podra hacer 1 entidad, el hilo tiene que esperar a que termina.
		       # Cuando este termine, usa 'release()' para darle el paso a la siguiente entidad, subiendo la suma de una vez.

	a=dato
	a+=1
	dato=a
	lock.release()

for i in range(3):
	t=threading.Thread(target=suma)
	t.start()
	hilos.append(t)

for i in hilos:
	i.join()
print(f"El MT imprime {dato}") # Ahora el main espera a los threads secundarios y luego imprime el resultado.
